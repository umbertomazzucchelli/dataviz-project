import xarray as xr
import pandas as pd
import numpy as np
import os

# Function to calculate trend (slope of linear regression) using xarray's polyfit
def calculate_trend(data_array, dim='time'):
    """Calculates the trend (slope) along a specified dimension using polyfit.

    Args:
        data_array (xr.DataArray): DataArray with time dimension and coordinates.
        dim (str): Name of the time dimension.

    Returns:
        xr.DataArray: DataArray containing the calculated trend (slope).
    """
    # Ensure the coordinate for the dimension is numeric for regression
    if np.issubdtype(data_array[dim].dtype, np.datetime64):
        # Convert datetime to year (or fraction of year for more precision if needed)
        # Using year as a float allows polyfit to work correctly.
        # Ensure it's a DataArray with the same dimension name as 'dim'
        time_numeric = xr.DataArray(
            data_array[dim].dt.year + (data_array[dim].dt.dayofyear - 1) / 365.25,
            coords={dim: data_array[dim]}, # Keep the original time coordinate
            name='time_numeric'
        )
    elif pd.api.types.is_numeric_dtype(data_array[dim].dtype):
        time_numeric = data_array[dim] # Assume it's already suitable numeric coord
    else:
        raise ValueError(f"Time coordinate '{dim}' must be datetime or numeric.")

    # Replace the original time coordinate with the numeric version for the fit
    # This avoids the need for the 'coord' argument in polyfit
    data_array_with_numeric_time = data_array.copy()
    # Assign the numeric time as a coordinate, potentially replacing the original
    # If the original dim name was 'time', this replaces it.
    data_array_with_numeric_time = data_array_with_numeric_time.assign_coords({dim: time_numeric})

    # Perform linear regression (degree=1 polynomial fit)
    # skipna=True handles NaNs in the data_array
    # Use the modified DataArray with the numeric time coordinate
    fit_coeffs = data_array_with_numeric_time.polyfit(dim=dim, deg=1, skipna=True, cov=False)['polyfit_coefficients']

    # Extract the slope (trend), which is the coefficient for degree 1
    slope = fit_coeffs.sel(degree=1)

    # Optionally, restore the original coordinate information if needed,
    # though the slope DataArray should retain the other coordinates (lat, lon).
    # slope = slope.assign_coords({dim: data_array[dim]}) # Not usually necessary

    return slope

# --- Main Script ---
if __name__ == "__main__":
    # File paths - Assuming script is run from the workspace root
    nc_file = "src/data/Global_TAVG_Gridded_5.nc"
    output_csv = "src/data/gridded_trends.csv"
    
    # Check if input file exists
    if not os.path.exists(nc_file):
        raise FileNotFoundError(f"Input NetCDF file not found: {nc_file}")

    print(f"Loading data from {nc_file}...")
    ds = None # Initialize ds to None
    try:
        # Use chunks for potentially large file
        ds = xr.open_dataset(nc_file, chunks={'time': 'auto'})
        # Try to standardize longitude coordinate if needed (0-360 -> -180 to 180)
        if 'lon' in ds.coords and ds['lon'].max() > 180:
             ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
             ds = ds.sortby('lon')
        if 'longitude' in ds.coords and ds['longitude'].max() > 180:
             ds = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180))
             ds = ds.sortby('longitude')
             
        print("Dataset loaded successfully.")
        print("Variables:", list(ds.variables))
        print("Coordinates:", list(ds.coords))
        
        # *** Determine temperature variable name ***
        possible_names = ['temperature_anomaly', 'temp_anomaly', 'tavg', 'tas', 'air_temperature']
        temp_var_name = None
        for name in possible_names:
            if name in ds.data_vars:
                temp_var_name = name
                print(f"Found temperature variable: '{temp_var_name}'")
                break
        
        if not temp_var_name:
             # If not found, try to guess based on attributes (units)
             for var in ds.data_vars:
                 if 'units' in ds[var].attrs and ('C' in ds[var].attrs['units'].upper() or 'K' in ds[var].attrs['units'].upper()):
                      # Check for names suggesting anomaly or temperature
                      if any(sub in var.lower() for sub in ['temp', 'tavg', 'tas']):
                          temp_var_name = var
                          print(f"Guessed temperature variable by attributes: '{temp_var_name}'")
                          break
        
        if not temp_var_name:
            raise ValueError(f"Could not determine temperature variable in {nc_file}. Inspected: {list(ds.data_vars)}")

        data = ds[temp_var_name]
        # Identify lat/lon coordinate names
        lat_coord_name = 'lat' if 'lat' in ds.coords else 'latitude'
        lon_coord_name = 'lon' if 'lon' in ds.coords else 'longitude'
        time_coord_name = 'time' # Assuming 'time'

        if lat_coord_name not in ds.coords or lon_coord_name not in ds.coords:
            raise ValueError(f"Could not find latitude/longitude coordinates. Found: {list(ds.coords)}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {nc_file}")
        exit()
    except ValueError as ve:
        print(f"Error: {ve}")
        if ds: ds.close()
        exit()
    except Exception as e:
        print(f"An unexpected error occurred during file loading or variable identification: {e}")
        if ds: ds.close()
        exit()

    # Define time periods
    period1_start, period1_end = "1901", "2023"
    period2_start, period2_end = "1994", "2023"

    try:
        print(f"Calculating trends for {period1_start}-{period1_end}...")
        data_period1 = data.sel({time_coord_name: slice(period1_start, period1_end)})
        # Ensure there's data for the period before calculating trend
        if data_period1[time_coord_name].size == 0:
            print(f"Warning: No data found for the period {period1_start}-{period1_end}. Skipping trend calculation.")
            trend_period1_C_year = xr.full_like(data.isel({time_coord_name: 0}, drop=True), np.nan) # Create NaN array
        else:
            trend_period1_C_year = calculate_trend(data_period1, dim=time_coord_name)

        print(f"Calculating trends for {period2_start}-{period2_end}...")
        data_period2 = data.sel({time_coord_name: slice(period2_start, period2_end)})
        if data_period2[time_coord_name].size == 0:
            print(f"Warning: No data found for the period {period2_start}-{period2_end}. Skipping trend calculation.")
            trend_period2_C_year = xr.full_like(data.isel({time_coord_name: 0}, drop=True), np.nan) # Create NaN array
        else:
            trend_period2_C_year = calculate_trend(data_period2, dim=time_coord_name)

        # Convert trends from °C/year to °C/decade
        # (°C/year) * (10 years/decade) = °C/decade
        conversion_factor = 10 
        trend_period1_C_decade = trend_period1_C_year * conversion_factor
        trend_period2_C_decade = trend_period2_C_year * conversion_factor

        # Combine trends into a single dataset
        trend_col_name1 = f'trend_{period1_start}_{period1_end}_C_decade'
        trend_col_name2 = f'trend_{period2_start}_{period2_end}_C_decade'
        trends_ds = xr.Dataset({
            trend_col_name1: trend_period1_C_decade,
            trend_col_name2: trend_period2_C_decade
        })

        # Convert to DataFrame for saving as CSV
        print(f"Converting trends to DataFrame...")
        # Ensure correct lat/lon names are used when converting
        trends_df = trends_ds.reset_coords().to_dataframe().reset_index()
        
        # Standardize column names after converting to DataFrame
        column_rename_map = {
            lat_coord_name: 'lat',
            lon_coord_name: 'lon'
        }
        # Only rename columns that actually exist in the DataFrame
        trends_df = trends_df.rename(columns={k: v for k, v in column_rename_map.items() if k in trends_df.columns})

        # Select only necessary columns and drop rows with all NaN trends
        required_cols = ['lat', 'lon', trend_col_name1, trend_col_name2]
        
        # Check if lat/lon columns exist before selecting
        if 'lat' not in trends_df.columns or 'lon' not in trends_df.columns:
             raise ValueError(f"Could not find 'lat' or 'lon' columns after converting to DataFrame. Columns found: {trends_df.columns.tolist()}")
             
        trends_df = trends_df[required_cols]
        trends_df = trends_df.dropna(subset=[trend_col_name1, trend_col_name2], how='all')

        # Save to CSV
        print(f"Saving trends to {output_csv}...")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        trends_df.to_csv(output_csv, index=False, float_format='%.4f')
        print(f"Trends successfully saved to {output_csv}.")

        # Optional: Print head of the DataFrame
        print("Preview of the trend data:")
        print(trends_df.head())

    except KeyError as ke:
        print(f"Error: A specified coordinate or variable name was not found: {ke}")
    except Exception as e:
        print(f"An unexpected error occurred during trend calculation or saving: {e}")
    finally:
        # Ensure the dataset is closed
        if ds:
            ds.close()
            print("Dataset closed.")
