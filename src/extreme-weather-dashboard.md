---
theme: dashboard
title: Extreme Weather Events
toc: false
sidebar: false
pager: false
---

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
  <div>
    <a href="/" style="text-decoration: none; color: #666; margin-right: 1rem;">Home</a>
    <a href="/global-temperature-dashboard" style="text-decoration: none; color: #666; margin-right: 1rem;">Global Temperature</a>
    <a href="/arctic-sea-ice-dashboard" style="text-decoration: none; color: #666; margin-right: 1rem;">Arctic Sea Ice</a>
    <a href="/extreme-weather-dashboard" style="text-decoration: none; color: #666; font-weight: bold; border-bottom: 2px solid #666; margin-right: 1rem;">Extreme Weather</a>
    <a href="/carbon-budget-dashboard" style="text-decoration: none; color: #666;">Carbon Budget</a>
  </div>
</div>

# When Weather Turns Wild 🌪️

Welcome to our exploration of nature's most powerful moments. As our planet warms, extreme weather events are becoming more frequent and intense. This dashboard takes you through storms, floods, droughts, and heat waves that are reshaping our understanding of "normal" weather. These aren't just statistics – they represent real impacts on communities around the world.

<!-- Load and transform the data -->

```js
// Load the storm location data - we now use location files instead of details files
// These files contain the geographical coordinates for all storm events

// Define year ranges
const startYear = 1951;
const endYear = 2024;

// Create explicit FileAttachment calls for specific years to ensure we have literal strings
// We'll use a subset of years that cover early, middle and recent periods
const stormLocations = [
  // 1950s
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1951_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1955_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1959_c20250401.csv.gz"),
  // 1960s
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1960_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1965_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1969_c20250401.csv.gz"),
  // 1970s
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1970_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1975_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1979_c20250401.csv.gz"),
  // 1980s
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1980_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1985_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1989_c20250401.csv.gz"),
  // 1990s
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1990_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1995_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d1999_c20250401.csv.gz"),
  // 2000s
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2000_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2005_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2009_c20250401.csv.gz"),
  // 2010s
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2010_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2015_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2019_c20250401.csv.gz"),
  // 2020s
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2020_c20240620.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2022_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_locations-ftp_v1.0_d2024_c20250401.csv.gz")
];

// Also load details files for better data completeness
const stormDetails = [
  // 1950s
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1951_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1955_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1959_c20250401.csv.gz"),
  // 1960s
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1960_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1965_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1969_c20250401.csv.gz"),
  // 1970s
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1970_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1975_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1979_c20250401.csv.gz"),
  // 1980s
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1980_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1985_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1989_c20250401.csv.gz"),
  // 1990s
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1990_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1995_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d1999_c20250401.csv.gz"),
  // 2000s
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2000_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2005_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2009_c20250401.csv.gz"),
  // 2010s
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2010_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2015_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2019_c20250401.csv.gz"),
  // 2020s
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2020_c20240620.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2022_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_details-ftp_v1.0_d2024_c20250401.csv.gz")
];

// Load fatality data for richer analysis
const stormFatalities = [
  // 1950s
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1951_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1955_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1959_c20250401.csv.gz"),
  // 1960s
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1960_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1965_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1969_c20250401.csv.gz"),
  // 1970s
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1970_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1975_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1979_c20250401.csv.gz"),
  // 1980s
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1980_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1985_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1989_c20250401.csv.gz"),
  // 1990s
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1990_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1995_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d1999_c20250401.csv.gz"),
  // 2000s
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2000_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2005_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2009_c20250401.csv.gz"),
  // 2010s
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2010_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2015_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2019_c20250401.csv.gz"),
  // 2020s
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2020_c20240620.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2022_c20250401.csv.gz"),
  FileAttachment("data/stormEvents/StormEvents_fatalities-ftp_v1.0_d2024_c20250401.csv.gz")
];

const precipitationData = FileAttachment("data/precipitation.csv");
```

```js
// Parse data - We're loading CSV files directly
// Add pako library for gzip decompression
import { inflate } from "https://cdn.jsdelivr.net/npm/pako@2.1.0/+esm";
import { csvParse } from "https://cdn.jsdelivr.net/npm/d3-dsv@3.0.1/+esm";

// Utility function to get the filename from a FileAttachment object
function getFileAttachmentName(fileAttachment) {
  // Try different properties that might contain the file path/name
  if (fileAttachment.name) {
    return fileAttachment.name;
  } else if (fileAttachment.url) {
    return fileAttachment.url;
  } else if (fileAttachment.path) {
    return fileAttachment.path;
  } else {
    // Try to extract from the toString() representation
    const str = fileAttachment.toString();
    // Look for patterns like FileAttachment("path/to/file.csv")
    const match = str.match(/FileAttachment\("([^"]+)"\)/);
    if (match && match[1]) {
      return match[1];
    }
    // If we get here, we couldn't determine the filename
    return null;
  }
}

// Utility function to detect if a file path is gzipped
function isGzipped(path) {
  if (!path) return false;
  return path.toLowerCase().endsWith('.gz');
}

// Utility function to decompress and parse a gzipped CSV file
async function loadCompressedCSV(fileAttachment) {
  try {
    // Get the file path for logging and potential fetch fallback
    const filePath = getFileAttachmentName(fileAttachment);
    console.log(`Attempting to load compressed CSV: ${filePath}`);
    
    let compressedBuffer;
    
    // Try to get the file as an array buffer, falling back to blob if necessary
    if (typeof fileAttachment.arrayBuffer === 'function') {
      compressedBuffer = await fileAttachment.arrayBuffer();
    } else if (typeof fileAttachment.blob === 'function') {
      // If arrayBuffer is not available, use blob and convert
      const blob = await fileAttachment.blob();
      compressedBuffer = await blob.arrayBuffer();
    } else if (typeof fileAttachment.text === 'function') {
      // Last resort: get as text and convert to Uint8Array
      const text = await fileAttachment.text();
      const encoder = new TextEncoder();
      compressedBuffer = encoder.encode(text).buffer;
    } else {
      throw new Error("FileAttachment object doesn't provide a suitable method to access raw data");
    }
    
    try {
      // Make sure we're working with a Uint8Array for pako
      const uint8Array = new Uint8Array(compressedBuffer);
      
      // Log some info about the compressed data for debugging
      console.log(`Compressed data length: ${uint8Array.length} bytes`);
      
      // Try various decompression methods
      let decompressedData;
      let text;
      
      try {
        // First try pako inflate without any special options
        decompressedData = inflate(uint8Array);
        text = new TextDecoder().decode(decompressedData);
        console.log("Decompression successful with pako's inflate");
      } catch (pakoError) {
        console.warn("Pako inflate failed, trying with windowBits: 15", pakoError);
        
        try {
          // Try with explicit windowBits
          decompressedData = inflate(uint8Array, { windowBits: 15 });
          text = new TextDecoder().decode(decompressedData);
          console.log("Decompression successful with pako's inflate with windowBits: 15");
        } catch (windowBitsError) {
          console.warn("Pako inflate with windowBits failed", windowBitsError);
          
          // Try alternative: direct CSV parsing
          try {
            console.log("Trying direct CSV parsing as fallback...");
            return await fileAttachment.csv();
          } catch (csvError) {
            console.warn("Direct CSV parsing failed too", csvError);
            
            // Last resort: try to download the file directly using fetch
            if (filePath) {
              console.log("Attempting to use fetch API to download and process the file");
              try {
                // Construct a relative URL to the data file
                const dataUrl = filePath.startsWith("/") ? filePath : `/${filePath}`;
                console.log(`Fetching from URL: ${dataUrl}`);
                
                const response = await fetch(dataUrl);
                if (!response.ok) throw new Error(`Fetch failed with status: ${response.status}`);
                
                const buffer = await response.arrayBuffer();
                // Try to decompress with pako again
                const decompressed = inflate(new Uint8Array(buffer));
                const fetchText = new TextDecoder().decode(decompressed);
                console.log("Fetch and decompress successful");
                return csvParse(fetchText);
              } catch (fetchError) {
                console.error("Fetch attempt also failed:", fetchError);
                throw fetchError;
              }
            } else {
              throw windowBitsError;
            }
          }
        }
      }
      
      // Check if we have actual CSV data
      if (!text.includes(',')) {
        console.error("Decompressed data doesn't appear to be CSV (no commas found)");
        console.log("First 100 chars:", text.substring(0, 100));
        throw new Error("Decompressed data is not in CSV format");
      }
      
      // Parse CSV
      return csvParse(text);
    } catch (decompressError) {
      console.error("All decompression attempts failed:", decompressError);
      throw decompressError;
    }
  } catch (error) {
    console.error("Error decompressing or parsing CSV:", error);
    throw error;
  }
}

// Process location data
async function processLocationData() {
  const allLocationData = [];
  const locationYears = [1951, 1955, 1959, 1960, 1965, 1969, 1970, 1975, 1979, 
                         1980, 1985, 1989, 1990, 1995, 1999, 2000, 2005, 2009,
                         2010, 2015, 2019, 2020, 2022, 2024];
  
  // Process each year's location data
  for (let i = 0; i < stormLocations.length; i++) {
    try {
      const year = locationYears[i];
      let locationData;
      
      try {
        // Try to load location data - check if gzipped
        const fileAttachment = stormLocations[i];
        const filePath = getFileAttachmentName(fileAttachment);
        
        if (isGzipped(filePath)) {
          // Handle gzipped file
          locationData = await loadCompressedCSV(fileAttachment);
        } else {
          // Use regular csv parsing for non-gzipped files
          locationData = await fileAttachment.csv();
        }
      } catch (error) {
        console.log(`Error loading location data for ${year}: ${error.message}`);
        locationData = []; // Set to empty array if file doesn't exist
      }
      
      // Skip if file is empty or only has header
      if (locationData.length <= 1) {
        console.log(`Skipping ${year} - no location data (only header)`);
        continue;
      }
      
      console.log(`Processing ${year} location data: ${locationData.length} records`);
      
      // Add year to each entry
      const processedData = locationData.map(d => ({
        ...d,
        YEAR: year
      }));
      
      allLocationData.push(...processedData);
    } catch (error) {
      console.log(`Error processing location data for year ${locationYears[i]}:`, error);
    }
  }
  
  return allLocationData;
}

// Process details data
async function processDetailsData() {
  const allDetailsData = [];
  const detailYears = [1951, 1955, 1959, 1960, 1965, 1969, 1970, 1975, 1979, 
                       1980, 1985, 1989, 1990, 1995, 1999, 2000, 2005, 2009,
                       2010, 2015, 2019, 2020, 2022, 2024];
  
  // Process each year's details data
  for (let i = 0; i < stormDetails.length; i++) {
    try {
      const year = detailYears[i];
      let detailsData;
      
      try {
        // Try to load details data - check if gzipped
        const fileAttachment = stormDetails[i];
        const filePath = getFileAttachmentName(fileAttachment);
        
        console.log(`Loading details data for ${year}, file: ${filePath}`);
        
        if (isGzipped(filePath)) {
          // Handle gzipped file
          console.log(`File ${filePath} is gzipped, using decompression`);
          detailsData = await loadCompressedCSV(fileAttachment);
        } else {
          // Use regular csv parsing for non-gzipped files
          console.log(`File ${filePath} is not gzipped, using direct CSV parsing`);
          detailsData = await fileAttachment.csv();
        }
        
        console.log(`Successfully loaded details data for ${year}: ${detailsData.length} records`);
      } catch (error) {
        console.error(`Error loading details data for ${year}:`, error);
        detailsData = []; // Set to empty array if file doesn't exist
      }
      
      // Skip if file is empty or only has header
      if (detailsData.length <= 1) {
        console.log(`Skipping ${year} - no details data (only header)`);
        continue;
      }
      
      console.log(`Processing ${year} details data: ${detailsData.length} records`);
      
      // Add year to each entry if not already present
      const processedData = detailsData.map(d => ({
        ...d,
        YEAR: d.YEAR || year
      }));
      
      allDetailsData.push(...processedData);
    } catch (error) {
      console.log(`Error processing details data for year ${detailYears[i]}:`, error);
    }
  }
  
  return allDetailsData;
}

// Process fatality data
async function processFatalityData() {
  const allFatalityData = [];
  const fatalityYears = [1951, 1955, 1959, 1960, 1965, 1969, 1970, 1975, 1979, 
                         1980, 1985, 1989, 1990, 1995, 1999, 2000, 2005, 2009,
                         2010, 2015, 2019, 2020, 2022, 2024];
  
  // Process each year's fatality data
  for (let i = 0; i < stormFatalities.length; i++) {
    try {
      const year = fatalityYears[i];
      let fatalityData;
      
      try {
        // Try to load fatality data - check if gzipped
        const fileAttachment = stormFatalities[i];
        const filePath = getFileAttachmentName(fileAttachment);
        
        if (isGzipped(filePath)) {
          // Handle gzipped file
          fatalityData = await loadCompressedCSV(fileAttachment);
        } else {
          // Use regular csv parsing for non-gzipped files
          fatalityData = await fileAttachment.csv();
        }
      } catch (error) {
        console.log(`Error loading fatality data for ${year}: ${error.message}`);
        fatalityData = []; // Set to empty array if file doesn't exist
      }
      
      // Skip if file is empty or only has header
      if (fatalityData.length <= 1) {
        console.log(`Skipping ${year} fatality data - no data (only header)`);
        continue;
      }
      
      console.log(`Processing ${year} fatality data: ${fatalityData.length} records`);
      
      // Add year to each entry
      const processedData = fatalityData.map(d => ({
        ...d,
        YEAR: year,
        // Ensure consistent property naming
        EVENT_ID: d.EVENT_ID,
        FATALITY_TYPE: d.FATALITY_TYPE
      }));
      
      allFatalityData.push(...processedData);
    } catch (error) {
      console.log(`Error processing fatality data for year ${fatalityYears[i]}:`, error);
    }
  }
  
  return allFatalityData;
}

// Parse location data
const locationData = await processLocationData();
console.log(`Loaded ${locationData.length} storm location records from ${startYear}-${endYear}`);
if (locationData.length > 0) {
  console.log('Sample location record:', locationData[0]);
}

// Parse details data
const detailsData = await processDetailsData();
console.log(`Loaded ${detailsData.length} storm details records from ${startYear}-${endYear}`);
if (detailsData.length > 0) {
  console.log('Sample details record:', detailsData[0]);
}

// Parse fatality data
const fatalityData = await processFatalityData();
console.log(`Loaded ${fatalityData.length} storm fatality records from ${startYear}-${endYear}`);
if (fatalityData.length > 0) {
  console.log('Sample fatality record:', fatalityData[0]);
}

// Try a simpler approach to load precipitation data
// First get the raw text
const precipitationRawText = await precipitationData.text();

// Skip the first few lines with comments (starting with #)
const precipitationLines = precipitationRawText.split('\n')
  .filter(line => line.trim() && !line.startsWith('#'));

// Extract header and data lines
const header = precipitationLines[0].split(',');
const dataRows = precipitationLines.slice(1);

// Parse into objects with proper numeric conversion
const precipitation = dataRows.map(line => {
  const values = line.split(',');
  const obj = {};
  
  header.forEach((col, i) => {
    // Convert numeric values and handle missing data
    const val = values[i];
    if (val === undefined || val === null || val === '') {
      obj[col] = null;
    } else if (col === 'Latitude' || col === 'Longitude' || col === 'Value' || 
               col === 'Anomaly' || col === 'Rank' || col === 'Mean') {
      const num = parseFloat(val);
      obj[col] = isNaN(num) ? null : num;
    } else {
      obj[col] = val;
    }
  });
  
  return obj;
}).filter(d => d.Latitude != null && d.Longitude != null && d.Anomaly != null);

// Log information about the precipitation data for debugging
console.log(`Loaded ${precipitation.length} precipitation data points`);
if (precipitation.length > 0) {
  console.log('Sample precipitation data point:', precipitation[0]);
}
```

```js
// Process and standardize data from both details and location files
function standardizeStormData(locationData, detailsData, fatalityData) {
  // Create a map of details data by EVENT_ID for easier lookup
  const detailsMap = new Map();
  detailsData.forEach(d => {
    detailsMap.set(d.EVENT_ID, d);
  });

  // Group fatality data by EVENT_ID for easier lookup
  const fatalitiesByEvent = new Map();
  fatalityData.forEach(d => {
    const eventId = d.EVENT_ID;
    if (!fatalitiesByEvent.has(eventId)) {
      fatalitiesByEvent.set(eventId, []);
    }
    fatalitiesByEvent.get(eventId).push(d);
  });
  
  // Process location data, supplementing with details when available
  const processedLocations = locationData.map(d => {
    // Get details for this event if available
    const details = detailsMap.get(d.EVENT_ID);
    
    // Handle missing values and convert to proper types
    const standardized = {};
    
    // Extract fields from location data and supplement with details
    standardized.YEAR = d.YEAR;
    standardized.EVENT_ID = d.EVENT_ID;
    standardized.EVENT_TYPE = d.EVENT_TYPE || (details ? details.EVENT_TYPE : null);
    standardized.STATE = d.STATE || (details ? details.STATE : null);
    
    // Set episode ID if available
    standardized.EPISODE_ID = d.EPISODE_ID || (details ? details.EPISODE_ID : null);
    
    // Extract YEARMONTH and convert to readable date format
    standardized.YEARMONTH = d.YEARMONTH || (details ? details.BEGIN_YEARMONTH : null);
    
    // Location data - handle both lat/lon formats
    standardized.BEGIN_LAT = d.LATITUDE !== undefined ? +d.LATITUDE || null : (+d.BEGIN_LAT || null);
    standardized.BEGIN_LON = d.LONGITUDE !== undefined ? +d.LONGITUDE || null : (+d.BEGIN_LON || null);
    standardized.END_LAT = d.LAT2 !== undefined ? +d.LAT2 || null : (+d.END_LAT || null);
    standardized.END_LON = d.LON2 !== undefined ? +d.LON2 || null : (+d.END_LON || null);
    
    // If location data is missing but we have details with coordinates, use those
    if ((standardized.BEGIN_LAT === null || standardized.BEGIN_LON === null) && details) {
      standardized.BEGIN_LAT = +details.BEGIN_LAT || null;
      standardized.BEGIN_LON = +details.BEGIN_LON || null;
      standardized.END_LAT = +details.END_LAT || null;
      standardized.END_LON = +details.END_LON || null;
    }
    
    // Begin and end date/time
    standardized.BEGIN_DATE_TIME = d.BEGIN_DATE_TIME || (details ? details.BEGIN_DATE_TIME : null);
    standardized.END_DATE_TIME = d.END_DATE_TIME || (details ? details.END_DATE_TIME : null);
    
    // Extract month and day for seasonal analysis
    if (standardized.BEGIN_DATE_TIME) {
      const dateMatch = standardized.BEGIN_DATE_TIME.match(/(\d+)-([A-Z]+)-(\d+)/);
      if (dateMatch) {
        // Convert month name to number
        const monthMap = {
          "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
          "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
        };
        standardized.MONTH = monthMap[dateMatch[2]] || null;
        standardized.DAY = parseInt(dateMatch[3]) || null;
      }
    } else if (details && details.BEGIN_YEARMONTH) {
      // Extract month from BEGIN_YEARMONTH (format: YYYYMM)
      const ym = details.BEGIN_YEARMONTH.toString();
      if (ym.length >= 6) {
        standardized.MONTH = parseInt(ym.substring(4, 6)) || null;
      }
    } else if (standardized.YEARMONTH) {
      // Extract month from YEARMONTH (format: YYYYMM)
      const ym = standardized.YEARMONTH.toString();
      if (ym.length >= 6) {
        standardized.MONTH = parseInt(ym.substring(4, 6)) || null;
      }
    }
    
    // Incorporate CZ_TYPE and CZ_NAME (county/zone info)
    standardized.CZ_TYPE = d.CZ_TYPE || (details ? details.CZ_TYPE : null);
    standardized.CZ_NAME = d.CZ_NAME || (details ? details.CZ_NAME : null);
    standardized.LOCATION = d.LOCATION || (details ? details.LOCATION : null);
    
    // Initialize casualty and damage fields
    standardized.DEATHS_DIRECT = 0;
    standardized.DEATHS_INDIRECT = 0;
    standardized.INJURIES_DIRECT = 0;
    standardized.INJURIES_INDIRECT = 0;
    standardized.DAMAGE_PROPERTY = "0";
    standardized.DAMAGE_CROPS = "0";
    
    // First check if we have data from the locations file
    if (d.DEATHS_DIRECT !== undefined) standardized.DEATHS_DIRECT = +d.DEATHS_DIRECT || 0;
    if (d.DEATHS_INDIRECT !== undefined) standardized.DEATHS_INDIRECT = +d.DEATHS_INDIRECT || 0;
    if (d.INJURIES_DIRECT !== undefined) standardized.INJURIES_DIRECT = +d.INJURIES_DIRECT || 0;
    if (d.INJURIES_INDIRECT !== undefined) standardized.INJURIES_INDIRECT = +d.INJURIES_INDIRECT || 0;
    if (d.DAMAGE_PROPERTY !== undefined) standardized.DAMAGE_PROPERTY = d.DAMAGE_PROPERTY || "0";
    if (d.DAMAGE_CROPS !== undefined) standardized.DAMAGE_CROPS = d.DAMAGE_CROPS || "0";
    
    // If not in location file, check the details file
    if (details) {
      if (standardized.DEATHS_DIRECT === 0 && details.DEATHS_DIRECT !== undefined) 
        standardized.DEATHS_DIRECT = +details.DEATHS_DIRECT || 0;
      if (standardized.DEATHS_INDIRECT === 0 && details.DEATHS_INDIRECT !== undefined) 
        standardized.DEATHS_INDIRECT = +details.DEATHS_INDIRECT || 0;
      if (standardized.INJURIES_DIRECT === 0 && details.INJURIES_DIRECT !== undefined) 
        standardized.INJURIES_DIRECT = +details.INJURIES_DIRECT || 0;
      if (standardized.INJURIES_INDIRECT === 0 && details.INJURIES_INDIRECT !== undefined) 
        standardized.INJURIES_INDIRECT = +details.INJURIES_INDIRECT || 0;
      if (standardized.DAMAGE_PROPERTY === "0" && details.DAMAGE_PROPERTY !== undefined) 
        standardized.DAMAGE_PROPERTY = details.DAMAGE_PROPERTY || "0";
      if (standardized.DAMAGE_CROPS === "0" && details.DAMAGE_CROPS !== undefined) 
        standardized.DAMAGE_CROPS = details.DAMAGE_CROPS || "0";
    }
    
    // Add fatality information
    const eventFatalities = fatalitiesByEvent.get(d.EVENT_ID) || [];
    if (eventFatalities.length > 0) {
      // If we have specific fatality records, use that data
      let directDeaths = 0;
      let indirectDeaths = 0;
      
      eventFatalities.forEach(f => {
        if (f.FATALITY_TYPE === "D") {
          directDeaths++;
        } else if (f.FATALITY_TYPE === "I") {
          indirectDeaths++;
        }
      });
      
      // Only override if we have actually found fatalities
      if (directDeaths > 0) standardized.DEATHS_DIRECT = directDeaths;
      if (indirectDeaths > 0) standardized.DEATHS_INDIRECT = indirectDeaths;
      
      // Extract additional fatality details
      standardized.FATALITY_LOCATIONS = eventFatalities.map(f => f.FATALITY_LOCATION).filter(Boolean);
    }
    
    // Include magnitude data if available
    standardized.MAGNITUDE = d.MAGNITUDE !== undefined ? +d.MAGNITUDE || null : 
                            (details && details.MAGNITUDE !== undefined ? +details.MAGNITUDE || null : null);
    standardized.MAGNITUDE_TYPE = d.MAGNITUDE_TYPE || (details ? details.MAGNITUDE_TYPE : null);
    
    return standardized;
  });
  
  // Process detailed events that don't have location data
  const locationEventIds = new Set(processedLocations.map(d => d.EVENT_ID));
  
  // For each details record that doesn't have a matching location record, create a new entry
  const missingLocationEvents = detailsData.filter(d => !locationEventIds.has(d.EVENT_ID)).map(details => {
    const standardized = {};
    
    standardized.YEAR = details.YEAR;
    standardized.EVENT_ID = details.EVENT_ID;
    standardized.EVENT_TYPE = details.EVENT_TYPE || null;
    standardized.STATE = details.STATE || null;
    standardized.EPISODE_ID = details.EPISODE_ID || null;
    standardized.YEARMONTH = details.BEGIN_YEARMONTH || null;
    
    // Location data from details
    standardized.BEGIN_LAT = +details.BEGIN_LAT || null;
    standardized.BEGIN_LON = +details.BEGIN_LON || null;
    standardized.END_LAT = +details.END_LAT || null;
    standardized.END_LON = +details.END_LON || null;
    
    // Begin and end date/time
    standardized.BEGIN_DATE_TIME = details.BEGIN_DATE_TIME || null;
    standardized.END_DATE_TIME = details.END_DATE_TIME || null;
    
    // Extract month and day for seasonal analysis
    if (standardized.BEGIN_DATE_TIME) {
      const dateMatch = standardized.BEGIN_DATE_TIME.match(/(\d+)-([A-Z]+)-(\d+)/);
      if (dateMatch) {
        // Convert month name to number
        const monthMap = {
          "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
          "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
        };
        standardized.MONTH = monthMap[dateMatch[2]] || null;
        standardized.DAY = parseInt(dateMatch[3]) || null;
      }
    } else if (details.BEGIN_YEARMONTH) {
      // Extract month from BEGIN_YEARMONTH (format: YYYYMM)
      const ym = details.BEGIN_YEARMONTH.toString();
      if (ym.length >= 6) {
        standardized.MONTH = parseInt(ym.substring(4, 6)) || null;
      }
    }
    
    // County/zone info
    standardized.CZ_TYPE = details.CZ_TYPE || null;
    standardized.CZ_NAME = details.CZ_NAME || null;
    
    // Casualty and damage fields
    standardized.DEATHS_DIRECT = +details.DEATHS_DIRECT || 0;
    standardized.DEATHS_INDIRECT = +details.DEATHS_INDIRECT || 0;
    standardized.INJURIES_DIRECT = +details.INJURIES_DIRECT || 0;
    standardized.INJURIES_INDIRECT = +details.INJURIES_INDIRECT || 0;
    standardized.DAMAGE_PROPERTY = details.DAMAGE_PROPERTY || "0";
    standardized.DAMAGE_CROPS = details.DAMAGE_CROPS || "0";
    
    // Add fatality information
    const eventFatalities = fatalitiesByEvent.get(details.EVENT_ID) || [];
    if (eventFatalities.length > 0) {
      // If we have specific fatality records, use that data
      let directDeaths = 0;
      let indirectDeaths = 0;
      
      eventFatalities.forEach(f => {
        if (f.FATALITY_TYPE === "D") {
          directDeaths++;
        } else if (f.FATALITY_TYPE === "I") {
          indirectDeaths++;
        }
      });
      
      // Only override if we have actually found fatalities
      if (directDeaths > 0) standardized.DEATHS_DIRECT = directDeaths;
      if (indirectDeaths > 0) standardized.DEATHS_INDIRECT = indirectDeaths;
      
      // Extract additional fatality details
      standardized.FATALITY_LOCATIONS = eventFatalities.map(f => f.FATALITY_LOCATION).filter(Boolean);
    }
    
    // Magnitude data
    standardized.MAGNITUDE = +details.MAGNITUDE || null;
    standardized.MAGNITUDE_TYPE = details.MAGNITUDE_TYPE || null;
    
    return standardized;
  });
  
  return [...processedLocations, ...missingLocationEvents];
}

// Combine all storm data
const allStormData = standardizeStormData(locationData, detailsData, fatalityData);

// Log dataset information
console.log(`Total storm events: ${allStormData.length}`);
console.log(`Year range: ${d3.min(allStormData, d => d.YEAR)} to ${d3.max(allStormData, d => d.YEAR)}`);
console.log(`Number of events with location data: ${allStormData.filter(d => d.BEGIN_LAT && d.BEGIN_LON).length}`);
console.log(`Most common event types: ${
  Array.from(d3.rollup(allStormData, v => v.length, d => d.EVENT_TYPE))
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([type, count]) => `${type} (${count})`)
    .join(', ')
}`);

// Function to clean and convert property damage values
function parseDamageValue(damageStr) {
  if (!damageStr || damageStr === "") return 0;
  
  // Extract numeric value and multiplier (K, M, B)
  const match = damageStr.match(/^(\d+\.?\d*)([KMB])?$/i);
  if (!match) return 0;
  
  const value = parseFloat(match[1]);
  const multiplier = match[2] ? match[2].toUpperCase() : "";
  
  // Apply multiplier
  switch (multiplier) {
    case "K": return value * 1000;
    case "M": return value * 1000000;
    case "B": return value * 1000000000;
    default: return value;
  }
}
```

```js
// Aggregate storm event counts by year and type
const eventsByYearAndType = d3.rollup(
  allStormData,
  v => v.length, // Count of events
  d => d.YEAR,    // Group by year
  d => d.EVENT_TYPE // Group by event type
);

// Convert to array format for easier plotting
const eventsByYearAndTypeArray = Array.from(eventsByYearAndType, ([year, types]) => {
  const entry = { year: +year };
  for (const [type, count] of types) {
    entry[type] = count;
  }
  return entry;
});

// Aggregate fatalities and injuries by year
const casualtiesByYear = d3.rollup(
  allStormData,
  v => ({
    directDeaths: d3.sum(v, d => +d.DEATHS_DIRECT || 0),
    indirectDeaths: d3.sum(v, d => +d.DEATHS_INDIRECT || 0),
    directInjuries: d3.sum(v, d => +d.INJURIES_DIRECT || 0),
    indirectInjuries: d3.sum(v, d => +d.INJURIES_INDIRECT || 0)
  }),
  d => d.YEAR
);

// Convert to array for plotting
const casualtiesByYearArray = Array.from(casualtiesByYear, ([year, data]) => ({
  year: +year,
  ...data
}));

// Aggregate property and crop damage by year
const damageByYear = d3.rollup(
  allStormData,
  v => ({
    propertyDamage: d3.sum(v, d => parseDamageValue(d.DAMAGE_PROPERTY)),
    cropDamage: d3.sum(v, d => parseDamageValue(d.DAMAGE_CROPS))
  }),
  d => d.YEAR
);

// Convert to array for plotting
const damageByYearArray = Array.from(damageByYear, ([year, data]) => ({
  year: +year,
  ...data
}));
```

```js
// Filter for events with major impacts (top 20%)
const significantEvents = allStormData.filter(d => {
  const propertyDamage = parseDamageValue(d.DAMAGE_PROPERTY);
  const deaths = (+d.DEATHS_DIRECT || 0) + (+d.DEATHS_INDIRECT || 0);
  const injuries = (+d.INJURIES_DIRECT || 0) + (+d.INJURIES_INDIRECT || 0);
  
  // Events with any fatalities, OR significant damage OR multiple injuries
  return deaths > 0 || propertyDamage >= 1000000 || injuries >= 5;
});

// Create a dataset for the map with lat/lon coordinates
const eventLocations = significantEvents
  .filter(d => d.BEGIN_LAT && d.BEGIN_LON) // Only events with location data
  .map(d => ({
    year: +d.YEAR,
    eventType: d.EVENT_TYPE,
    latitude: +d.BEGIN_LAT,
    longitude: +d.BEGIN_LON,
    deaths: (+d.DEATHS_DIRECT || 0) + (+d.DEATHS_INDIRECT || 0),
    injuries: (+d.INJURIES_DIRECT || 0) + (+d.INJURIES_INDIRECT || 0),
    propertyDamage: parseDamageValue(d.DAMAGE_PROPERTY),
    cropDamage: parseDamageValue(d.DAMAGE_CROPS),
    state: d.STATE
  }));
```

<!-- Create key visualizations -->

```js
// Fetch country boundaries for the map overlay
const countriesPromise = fetch("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(response => response.json());
const countries = await countriesPromise;
const land = topojson.feature(countries, countries.objects.land);
const statesPromise = fetch("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json").then(response => response.json());
const states = await statesPromise;
const stateFeatures = topojson.feature(states, states.objects.states);
```

```js
function stormEventTimeline(data, {width} = {}) {
  // Get the top 10 most frequent event types
  const allEventTypes = new Set();
  data.forEach(d => {
    Object.keys(d).forEach(key => {
      if (key !== 'year') allEventTypes.add(key);
    });
  });
  
  // Convert each year's data into the format needed for a stacked bar chart
  const stackData = [];
  data.forEach(yearData => {
    const year = yearData.year;
    allEventTypes.forEach(type => {
      if (type !== 'year' && yearData[type]) {
        stackData.push({
          year,
          type,
          count: yearData[type]
        });
      }
    });
  });
  
  // Sort event types by total count
  const typeTotals = d3.rollup(
    stackData,
    v => d3.sum(v, d => d.count),
    d => d.type
  );
  
  const sortedTypes = Array.from(typeTotals, ([type, total]) => ({type, total}))
    .sort((a, b) => b.total - a.total)
    .slice(0, 8) // Top 8 types
    .map(d => d.type);
  
  // Filter data to only include top types
  const filteredData = stackData.filter(d => sortedTypes.includes(d.type));
  
  return Plot.plot({
    title: "Frequency of Extreme Weather Events by Type (1951-2024)",
    subtitle: "Showing the eight most common event types recorded in the NOAA database",
    width,
    height: 500,
    x: {
      label: "Year",
      tickFormat: "d"
    },
    y: {
      label: "Number of Events",
      grid: true
    },
    color: {
      legend: true
    },
    marks: [
      Plot.barY(filteredData, {
        x: "year",
        y: "count",
        fill: "type",
        tip: true,
        title: d => `${d.type}: ${d.count} events in ${d.year}`
      })
    ]
  });
}
```

```js
function interactiveStormEventMap(data, {width} = {}) {
  // Add this log:
  console.log("Data received by interactiveStormEventMap:", data.slice(0, 10)); // Log first 10 records
  const eventTypesInData = Array.from(new Set(data.map(d => d.eventType)));
  console.log("Raw unique eventTypes found in data:", eventTypesInData);

  // Define time periods for comparison
  const pastPeriod = [1970, 1999]; // Past: 1970-1999
  const presentPeriod = [2000, 2024]; // Present: 2000-2024

  // --- Start Change: Filter types present in BOTH periods ---
  // Filter data for each period
  const pastData = data.filter(d => d.year >= pastPeriod[0] && d.year <= pastPeriod[1]);
  const presentData = data.filter(d => d.year >= presentPeriod[0] && d.year <= presentPeriod[1]);

  // Get unique, non-empty types from each period
  const pastTypes = new Set(pastData.map(d => d.eventType).filter(type => type && type.length > 0));
  const presentTypes = new Set(presentData.map(d => d.eventType).filter(type => type && type.length > 0));

  // Find the intersection (types present in both)
  const commonEventTypes = [...pastTypes].filter(type => presentTypes.has(type))
    .sort((a, b) => a.localeCompare(b));

  // Use commonEventTypes for the dropdown
  const eventTypes = commonEventTypes; 
  // --- End Change ---

  console.log(`Found ${eventTypes.length} unique event types present in BOTH periods for filtering`);
  console.log("Filtered and sorted event types (common to both periods):", eventTypes);

  // Create a state object to track filter settings
  const state = {
    eventType: "all" // Default to all event types
  };

  // Create filtered datasets
  function getFilteredData() {
    let filtered = [...data]; // Start with all data

    // Apply event type filter
    if (state.eventType !== "all") {
      filtered = filtered.filter(d => d.eventType === state.eventType);
    }

    return filtered;
  }

  // Count events by state or prepare appropriate metric data
  function aggregateByState(filteredData) {
    // Always aggregate by property damage (in millions)
    return d3.rollup(
       filteredData,
       v => d3.sum(v, d => d.propertyDamage) / 1e6, // Convert to millions
       d => d.state
     );
  }

  // Color scale based on metric
  function getColorScale(stateData) {
    const colorLabel = "Damage (Millions $)";

    return {
      type: "quantize",
      n: 9,
      scheme: "Blues",
      domain: [0, d3.max(stateData, d => d.value) || 1],
      legend: false, // Always hide the legend
      label: colorLabel
    };
  }

  // Create the plot
  function createPlot() {
    const filteredData = getFilteredData();
    const eventsByState = aggregateByState(filteredData);

    // --- Start Change: Filter dots for minimum damage and create radius scale ---
    // Get the density setting from the slider (default to 20M if not set)
    const densityThreshold = parseFloat(mainContainer.querySelector('#density-slider')?.value || 20);
    // Convert from millions to actual value (e.g., 20M = 20,000,000)
    const damageThreshold = densityThreshold * 1000000;
    
    // Filter data based on the threshold
    const dotData = filteredData.filter(d => d.propertyDamage >= damageThreshold);
    console.log(`Showing ${dotData.length} events with damage >= $${densityThreshold}M`);
    
    let radiusScale = () => 3; // Default fixed radius
    // Always scale radius by damage if data exists
    if (dotData.length > 0) { 
      const damageExtent = d3.extent(dotData, d => d.propertyDamage);
      // Ensure extent is valid and starts at threshold
      const minDamage = Math.max(damageThreshold, damageExtent[0] || damageThreshold);
      const maxDamage = damageExtent[1] || minDamage;
      
      radiusScale = d3.scaleSqrt()
                      .domain([minDamage, maxDamage]) // Domain from threshold to max
                      .range([2, 15]); // Reduced max radius from 20px to 15px
    }
    // --- End Change ---
    
    const stateEvents = Array.from(eventsByState, ([state, value]) => ({
      state,
      value
    }));

    // --- Start Change: Create color scale once ---
    const scaleConfig = getColorScale(stateEvents);
    let colorScale; 
    // Ensure the domain has valid numbers
    const domain = scaleConfig.domain.map(d => isNaN(d) ? 0 : d); 
    if (domain && domain.length >= 2 && d3.schemeBlues[scaleConfig.n]) {
        colorScale = d3.scaleQuantize()
                       .domain(domain) 
                       .range(d3.schemeBlues[scaleConfig.n]); 
    } else {
        console.warn("Could not create valid color scale. Using default.", {scaleConfig});
        // Fallback scale
        colorScale = () => "#cccccc"; 
    }
    // --- End Change ---

    let title = "Locations of";
    if (state.eventType !== "all") {
      title += ` ${state.eventType}`;
    } else {
      title += " Major Storm Events";
    }

    title += ` (${pastPeriod[0]}-${presentPeriod[1]})`;

    return Plot.plot({
      title,
      width,
      height: 600,
      projection: "albers",
      color: getColorScale(stateEvents),
      marks: [
        Plot.geo(stateFeatures, {
          fill: d => {
            const stateEvent = stateEvents.find(e => e.state === d.properties.name);
            return stateEvent ? stateEvent.value : 0;
          },
          stroke: "#fff",
          strokeWidth: 0.5,
          title: d => {
            const stateEvent = stateEvents.find(e => e.state === d.properties.name);
            let titleText = `${d.properties.name}: `;
            if (stateEvent) {
              // Always show damage in title
              titleText += `$${stateEvent.value.toFixed(1)}M in damages`;
            } else {
              titleText += "No data";
            }
            return titleText;
          }
        }),
        Plot.dot(dotData, { // Use filtered dotData here
          x: "longitude",
          y: "latitude",
          r: d => {
            // --- Start Change: Use radius scale ---
            // Always use radius scale based on property damage
            return radiusScale(d.propertyDamage);
            // --- End Change ---
          },
          fill: d => {
            // Color by time period: blue for past, red for present
            return d.year >= 1970 && d.year <= 1999 ? "#4682b4" : "#e63946";
          },
          fillOpacity: 0.5, // Reduced opacity from 0.7 to 0.5
          stroke: "#000",
          strokeOpacity: 0.2, // Reduced stroke opacity from 0.3 to 0.2
          tip: true,
          title: d => `${d.eventType} (${d.year})\nState: ${d.state}\nDeaths: ${d.deaths}\nDamage: $${(d.propertyDamage/1000000).toFixed(1)}M`
        })
      ]
    });
  }

  // --- Start New Structure ---

  // 1. Create the main container structure
  const mainContainer = html`
    <div>
      <form style="margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 1rem;">
        <div>
          <label for="event-select">Event Type: </label>
          <select id="event-select" style="min-width: 200px; padding: 5px;">
            <option value="all">All Event Types</option>
            <!-- Options will be added programmatically below -->
          </select>
        </div>
        
        <div style="flex-basis: 100%;">
          <label for="density-slider">Min Damage Threshold: $<span id="density-value">20</span>M</label>
          <input type="range" id="density-slider" min="1" max="100" value="20" style="width: 300px;">
        </div>
      </form>
      
      <!-- Legend for time periods -->
      <div style="display: flex; gap: 15px; margin-bottom: 10px; font-size: 0.9em;">
        <div><span style="display: inline-block; width: 15px; height: 15px; background-color: #4682b4; border-radius: 50%; margin-right: 5px;"></span> Past (1970-1999)</div>
        <div><span style="display: inline-block; width: 15px; height: 15px; background-color: #e63946; border-radius: 50%; margin-right: 5px;"></span> Present (2000-2024)</div>
      </div>
      
      <div class="map-container-placeholder" style="min-height: 600px;"></div> <!-- Added min-height -->
      <div style="font-size: 0.9em; margin-top: 0.5rem; color: #666;">
        Tip: Use the "Event Type" dropdown to filter by specific event types. Adjust the damage threshold to reduce crowding.
      </div>
    </div>
  `;

  // 2. Populate the event type dropdown within the container
  const eventSelect = mainContainer.querySelector('#event-select');
  if (eventSelect) {
    eventTypes.forEach(type => {
      const option = document.createElement('option');
      option.value = type;
      option.textContent = type;
      eventSelect.appendChild(option);
    });
    console.log(`Successfully added ${eventTypes.length} options to #event-select`);
  } else {
    console.error("Could not find #event-select element to populate.");
  }

  // 3. Get the placeholder for the map within the container
  const mapContainer = mainContainer.querySelector('.map-container-placeholder');

  // 4. Define function to update the map within the placeholder
  function updateMap() {
    if (mapContainer) {
        mapContainer.innerHTML = ''; // Clear previous map
        mapContainer.append(createPlot()); // Add new map
    } else {
        console.error("Map container not found for update.");
    }
  }

  // 5. Add event listeners to controls within the main container
  const densitySlider = mainContainer.querySelector('#density-slider');
  const densityValue = mainContainer.querySelector('#density-value');

  if (eventSelect) { // Reuse the variable from step 2
    eventSelect.addEventListener('change', (event) => {
      state.eventType = event.target.value;
      console.log(`Event type changed to: ${state.eventType}`);
      updateMap();
    });
  } else {
     console.error("Could not find #event-select to attach listener.");
  }
  
  if (densitySlider && densityValue) {
    // Update the displayed value when slider changes
    densitySlider.addEventListener('input', (event) => {
      densityValue.textContent = event.target.value;
    });
    
    // Only update the map when sliding stops
    densitySlider.addEventListener('change', () => {
      updateMap();
    });
  } else {
    console.error("Could not find density slider or value elements");
  }

  // 6. Initial map rendering
  updateMap();

  // 7. Return the fully assembled container
  return mainContainer;

  // --- End New Structure ---
}

// Function to prepare data for the map
function prepareStormMapData(allStormData) {
  // Filter for events with major impacts
  const significantEvents = allStormData.filter(d => {
    const propertyDamage = parseDamageValue(d.DAMAGE_PROPERTY);
    const deaths = (+d.DEATHS_DIRECT || 0) + (+d.DEATHS_INDIRECT || 0);
    const injuries = (+d.INJURIES_DIRECT || 0) + (+d.INJURIES_INDIRECT || 0);
    
    // Events with any fatalities, OR significant damage OR multiple injuries
    return deaths > 0 || propertyDamage >= 1000000 || injuries >= 5;
  });

  // Create a dataset for the map with lat/lon coordinates
  return significantEvents
    .filter(d => d.BEGIN_LAT && d.BEGIN_LON) // Only events with location data
    .map(d => ({
      year: +d.YEAR,
      eventType: d.EVENT_TYPE,
      latitude: +d.BEGIN_LAT,
      longitude: +d.BEGIN_LON,
      deaths: (+d.DEATHS_DIRECT || 0) + (+d.DEATHS_INDIRECT || 0),
      injuries: (+d.INJURIES_DIRECT || 0) + (+d.INJURIES_INDIRECT || 0),
      propertyDamage: parseDamageValue(d.DAMAGE_PROPERTY),
      cropDamage: parseDamageValue(d.DAMAGE_CROPS),
      state: d.STATE
    }));
}
```

```js
function stormCostsTimeline(casualties, damages, {width} = {}) {
  // Join casualties and damages data
  const years = new Set([...casualties.map(d => d.year), ...damages.map(d => d.year)]);
  const combinedData = Array.from(years).map(year => {
    const casualtyData = casualties.find(d => d.year === year) || {};
    const damageData = damages.find(d => d.year === year) || {};
    
    return {
      year,
      directDeaths: casualtyData.directDeaths || 0,
      indirectDeaths: casualtyData.indirectDeaths || 0,
      directInjuries: casualtyData.directInjuries || 0,
      indirectInjuries: casualtyData.indirectInjuries || 0,
      propertyDamage: damageData.propertyDamage || 0,
      cropDamage: damageData.cropDamage || 0
    };
  }).sort((a, b) => a.year - b.year);
  
  return Plot.plot({
    title: "Economic and Human Costs of Extreme Weather Events (1951-2024)",
    subtitle: "Annual property damage (bars) and fatalities (red line) from severe weather",
    width,
    height: 500,
    marginRight: 120,
    grid: true,
    x: {
      label: "Year",
      tickFormat: "d"
    },
    y: {
      label: "Property & Crop Damage (Billions $)",
      transform: d => d / 1e9
    },
    y2: {
      label: "Deaths",
      grid: true
    },
    color: {
      legend: true
    },
    marks: [
      Plot.barY(combinedData, {
        x: "year",
        y: d => d.propertyDamage + d.cropDamage,
        fill: "#3b88c4",
        fillOpacity: 0.7,
        title: d => `Year: ${d.year}`
      }),
      Plot.lineY(combinedData, {
        x: "year",
        y: d => d.directDeaths + d.indirectDeaths,
        stroke: "red",
        strokeWidth: 3,
        y2: true
      }),
      Plot.dot(combinedData, {
        x: "year",
        y: d => d.directDeaths + d.indirectDeaths,
        stroke: "red",
        r: 4,
        y2: true,
        title: d => `Fatalities: ${d.directDeaths + d.indirectDeaths}`
      })
    ]
  });
}
```

```js
function precipitationAnomalyMap(data, {width} = {}) {
  // Apply filter to data to remove any problematic entries
  const validData = data.filter(d => 
    d && 
    d.Latitude !== null && !isNaN(d.Latitude) && 
    d.Longitude !== null && !isNaN(d.Longitude) && 
    d.Anomaly !== null && !isNaN(d.Anomaly) && 
    d.Anomaly > -9000
  );
  
  console.log(`Valid data points for visualization: ${validData.length}`);
  
  // Use a fixed range for color scale
  const maxAbsAnomaly = 3;
  
  return Plot.plot({
    width,
    height: 500,
    projection: "equal-earth",
    style: {
      backgroundColor: "#111",
      color: "white"
    },
    color: {
      type: "diverging",
      scheme: "RdBu",
      reverse: true,
      domain: [-maxAbsAnomaly, 0, maxAbsAnomaly],
      legend: true,
      label: "Precipitation Anomaly (mm)"
    },
    marks: [
      // Simple base map
      Plot.frame({fill: "#111"}),
      
      // Land background
      Plot.geo(land, {
        fill: "#222",
        stroke: "none"
      }),
      
      // Data points as simple dots
      Plot.dot(validData, {
        x: "Longitude",
        y: "Latitude",
        fill: "Anomaly",
        r: 3.5,
        opacity: 0.9
      }),
      
      // Country outlines
      Plot.geo(land, {
        stroke: "white",
        strokeWidth: 0.5,
        strokeOpacity: 0.5,
        fill: "none"
      })
    ]
  });
}
```

```js
// Function to compare event frequencies across decades
function decadalEventComparison(data, {width} = {}) {
  // Create decade groups (1990s, 2000s, 2010s, 2020s)
  const byDecade = d3.rollup(
    data,
    v => v.length,
    d => Math.floor(d.YEAR / 10) * 10, // Group by decade
    d => d.EVENT_TYPE
  );
  
  // Get the top 10 most frequent event types across all decades
  const allEvents = data.map(d => d.EVENT_TYPE);
  const eventCounts = d3.rollup(allEvents, v => v.length, d => d);
  const top10Events = Array.from(eventCounts, ([type, count]) => ({type, count}))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10)
    .map(d => d.type);
  
  // Create a dataset for the chart
  const decadeData = [];
  for (const [decade, events] of byDecade) {
    for (const [type, count] of events) {
      if (top10Events.includes(type)) {
        decadeData.push({
          decade: `${decade}s`,
          type,
          count,
          // Calculate per-year rate to normalize decades with partial data
          eventsPerYear: decade === 2020 ? count / 5 : count / 10  // 2020s has ~5 years of data so far
        });
      }
    }
  }
  
  // Sort by decade
  decadeData.sort((a, b) => a.decade.localeCompare(b.decade));
  
  // Calculate event trend changes between decades for top events
  const trendAnalysis = [];
  top10Events.forEach(eventType => {
    const eventsByDecade = decadeData.filter(d => d.type === eventType);
    
    // Sort by decade chronologically
    eventsByDecade.sort((a, b) => a.decade.localeCompare(b.decade));
    
    // Calculate percentage changes between consecutive decades
    for (let i = 1; i < eventsByDecade.length; i++) {
      const prevDecade = eventsByDecade[i-1];
      const currDecade = eventsByDecade[i];
      
      // Use events per year for fair comparison
      const percentChange = ((currDecade.eventsPerYear - prevDecade.eventsPerYear) / prevDecade.eventsPerYear) * 100;
      
      trendAnalysis.push({
        eventType,
        fromDecade: prevDecade.decade,
        toDecade: currDecade.decade,
        percentChange,
        increasing: percentChange > 0
      });
    }
  });
  
  // Get the events with the largest increases and decreases
  const topIncreases = trendAnalysis
    .filter(d => d.percentChange > 0)
    .sort((a, b) => b.percentChange - a.percentChange)
    .slice(0, 5);
  
  const topDecreases = trendAnalysis
    .filter(d => d.percentChange < 0)
    .sort((a, b) => a.percentChange - b.percentChange)
    .slice(0, 5);
  
  return Plot.plot({
    width,
    height: 500,
    marginLeft: 120,
    x: {
      grid: true,
      label: "Number of Events"
    },
    y: {
      label: null
    },
    color: {
      legend: true
    },
    marks: [
      Plot.barX(decadeData, {
        x: "count",
        y: "decade",
        fill: "type",
        sort: {y: "x", reverse: true}
      }),
      Plot.ruleX([0])
    ]
  });
}

// Function to analyze damage costs across decades
function decadalDamageComparison(data, {width} = {}) {
  // Group damage by decade
  const byDecade = d3.rollup(
    data,
    v => ({
      propertyDamage: d3.sum(v, d => parseDamageValue(d.DAMAGE_PROPERTY)),
      cropDamage: d3.sum(v, d => parseDamageValue(d.DAMAGE_CROPS)),
      totalDamage: d3.sum(v, d => parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS)),
      eventCount: v.length,
      // Calculate number of billion-dollar events
      billionDollarEvents: v.filter(d => 
        parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS) >= 1e9
      ).length
    }),
    d => Math.floor(d.YEAR / 10) * 10 // Group by decade
  );
  
  // Convert to array for plotting
  const decadeData = Array.from(byDecade, ([decade, stats]) => ({
    decade: `${decade}s`,
    propertyDamage: stats.propertyDamage,
    cropDamage: stats.cropDamage,
    totalDamage: stats.totalDamage,
    eventCount: stats.eventCount,
    billionDollarEvents: stats.billionDollarEvents,
    // Calculate average damage per event
    avgDamagePerEvent: stats.totalDamage / stats.eventCount
  })).sort((a, b) => a.decade.localeCompare(b.decade));
  
  // For 2020s, normalize values to estimate full decade (if it's partial data)
  // Assuming we have data up to 2024, we multiply by 10/5 = 2
  const last = decadeData[decadeData.length - 1];
  if (last && last.decade === "2020s") {
    // Current year in the dataset minus 2020 gives number of years in current decade
    const yearsInCurrentDecade = 5; // Approximating for 2020-2024
    const scaleFactor = 10 / yearsInCurrentDecade;
    
    // Add projected values
    last.projectedTotalDamage = last.totalDamage * scaleFactor;
    last.projectedBillionDollarEvents = last.billionDollarEvents * scaleFactor;
  }
  
  return {
    // Chart for total damage by decade
    damageChart: Plot.plot({
      title: "",
      width,
      height: 300,
      x: {
        label: "Decade"
      },
      y: {
        label: "Damage (Billions $)",
        transform: d => d / 1e9,
        grid: true
      },
      color: {
        domain: ["Property Damage", "Crop Damage"],
        range: ["#3b88c4", "#66bb6a"]
      },
      marks: [
        Plot.barY(decadeData, {
          x: "decade",
          y: "propertyDamage",
          fill: "#3b88c4",
          title: d => `Property Damage: $${(d.propertyDamage/1e9).toFixed(1)} billion`
        }),
        Plot.barY(decadeData, {
          x: "decade",
          y: "cropDamage",
          fill: "#66bb6a",
          title: d => `Crop Damage: $${(d.cropDamage/1e9).toFixed(1)} billion`
        }),
        // Add a projection for the 2020s if it's partial data
        ...(decadeData[decadeData.length - 1]?.decade === "2020s" ? [
          Plot.barY([decadeData[decadeData.length - 1]], {
            x: "decade",
            y: d => d.projectedTotalDamage - d.totalDamage,
            fill: "url(#diagonal-stripe-1)",
            fillOpacity: 0.5,
            title: d => `Projected additional damage: $${((d.projectedTotalDamage - d.totalDamage)/1e9).toFixed(1)} billion`
          })
        ] : [])
      ]
    }),
    
    // Chart for billion-dollar disasters by decade
    billionDollarChart: Plot.plot({
      title: "Billion-Dollar Weather Disasters by Decade",
      width,
      height: 300,
      x: {
        label: "Decade"
      },
      y: {
        label: "Number of Events",
        grid: true
      },
      marks: [
        Plot.barY(decadeData, {
          x: "decade",
          y: "billionDollarEvents",
          fill: "#ff6666",
          title: d => `${d.billionDollarEvents} billion-dollar disasters`
        }),
        // Add a projection for the 2020s if it's partial data
        ...(decadeData[decadeData.length - 1]?.decade === "2020s" ? [
          Plot.barY([decadeData[decadeData.length - 1]], {
            x: "decade",
            y: d => d.projectedBillionDollarEvents - d.billionDollarEvents,
            fill: "url(#diagonal-stripe-2)",
            fillOpacity: 0.5,
            title: d => `Projected additional events: ${Math.round(d.projectedBillionDollarEvents - d.billionDollarEvents)}`
          })
        ] : [])
      ]
    })
  };
}

// Function to analyze event intensity changes over time
function intensityChangeAnalysis(data, {width} = {}) {
  // Filter for events with magnitude data
  const eventsWithMagnitude = data.filter(d => 
    d.MAGNITUDE !== null && 
    d.MAGNITUDE_TYPE !== null && 
    ["TORNADO", "HURRICANE", "THUNDERSTORM WIND", "FLASH FLOOD", "HAIL"].includes(d.EVENT_TYPE)
  );
  
  console.log(`Events with magnitude data: ${eventsWithMagnitude.length}`);
  console.log(`Event types with magnitude data: ${[...new Set(eventsWithMagnitude.map(d => d.EVENT_TYPE))].join(", ")}`);
  
  // Group by event type, year and calculate average magnitude
  const magnitudeByYearType = d3.rollup(
    eventsWithMagnitude,
    v => ({
      avgMagnitude: d3.mean(v, d => d.MAGNITUDE),
      maxMagnitude: d3.max(v, d => d.MAGNITUDE),
      count: v.length,
      // Calculate proportion of high-intensity events (event-specific thresholds)
      highIntensityCount: v.filter(d => {
        if (d.EVENT_TYPE === "TORNADO" && d.MAGNITUDE >= 3) return true; // EF3+ tornadoes
        if (d.EVENT_TYPE === "HURRICANE" && d.MAGNITUDE >= 3) return true; // Cat 3+ hurricanes
        if (d.EVENT_TYPE === "THUNDERSTORM WIND" && d.MAGNITUDE >= 65) return true; // Severe thunderstorm wind
        if (d.EVENT_TYPE === "FLASH FLOOD" && d.MAGNITUDE >= 2) return true; // Moderate+ flash floods
        if (d.EVENT_TYPE === "HAIL" && d.MAGNITUDE >= 2) return true; // Hail 2"+ diameter
        return false;
      }).length
    }),
    d => d.EVENT_TYPE,
    d => d.YEAR
  );
  
  // Convert to array for plotting
  const magnitudeData = [];
  for (const [type, years] of magnitudeByYearType) {
    for (const [year, stats] of years) {
      magnitudeData.push({
        type,
        year,
        avgMagnitude: stats.avgMagnitude,
        maxMagnitude: stats.maxMagnitude,
        count: stats.count,
        highIntensityCount: stats.highIntensityCount,
        highIntensityPct: (stats.highIntensityCount / stats.count) * 100
      });
    }
  }
  
  // Sort by year for trend analysis
  magnitudeData.sort((a, b) => a.year - b.year);
  
  // Calculate average magnitude by decade for each event type
  const decadeAvgMagnitude = d3.rollup(
    eventsWithMagnitude,
    v => ({
      avgMagnitude: d3.mean(v, d => d.MAGNITUDE),
      maxMagnitude: d3.max(v, d => d.MAGNITUDE),
      count: v.length,
      // Calculate proportion of high-intensity events (event-specific thresholds)
      highIntensityCount: v.filter(d => {
        if (d.EVENT_TYPE === "TORNADO" && d.MAGNITUDE >= 3) return true; // EF3+ tornadoes
        if (d.EVENT_TYPE === "HURRICANE" && d.MAGNITUDE >= 3) return true; // Cat 3+ hurricanes
        if (d.EVENT_TYPE === "THUNDERSTORM WIND" && d.MAGNITUDE >= 65) return true; // Severe thunderstorm wind
        if (d.EVENT_TYPE === "FLASH FLOOD" && d.MAGNITUDE >= 2) return true; // Moderate+ flash floods
        if (d.EVENT_TYPE === "HAIL" && d.MAGNITUDE >= 2) return true; // Hail 2"+ diameter
        return false;
      }).length
    }),
    d => d.EVENT_TYPE,
    d => Math.floor(d.YEAR / 10) * 10
  );
  
  // Convert to array and calculate percent change between decades
  const decadeTrends = [];
  for (const [type, decades] of decadeAvgMagnitude) {
    const decadeValues = Array.from(decades, ([decade, stats]) => ({
      decade,
      avgMagnitude: stats.avgMagnitude,
      maxMagnitude: stats.maxMagnitude,
      count: stats.count,
      highIntensityCount: stats.highIntensityCount,
      highIntensityPct: (stats.highIntensityCount / stats.count) * 100
    })).sort((a, b) => a.decade - b.decade);
    
    // Calculate percent changes between consecutive decades
    for (let i = 1; i < decadeValues.length; i++) {
      const prevDecade = decadeValues[i-1];
      const currDecade = decadeValues[i];
      
      // Calculate multiple trend metrics
      const avgMagnitudePctChange = ((currDecade.avgMagnitude - prevDecade.avgMagnitude) / prevDecade.avgMagnitude) * 100;
      const maxMagnitudePctChange = ((currDecade.maxMagnitude - prevDecade.maxMagnitude) / prevDecade.maxMagnitude) * 100;
      const highIntensityPctChange = currDecade.highIntensityPct - prevDecade.highIntensityPct;
      
      decadeTrends.push({
        type,
        fromDecade: `${prevDecade.decade}s`,
        toDecade: `${currDecade.decade}s`,
        avgMagnitudePctChange,
        maxMagnitudePctChange,
        highIntensityPctChange,
        // Use the most representative change metric based on event type
        primaryChange: type === "TORNADO" || type === "HURRICANE" ? highIntensityPctChange : avgMagnitudePctChange
      });
    }
  }
  
  // Calculate extreme event frequency changes
  console.log("High-intensity event percentage changes by type:");
  decadeTrends.forEach(trend => {
    console.log(`${trend.type}: ${trend.fromDecade} to ${trend.toDecade}: High-intensity events ${trend.highIntensityPctChange > 0 ? '+' : ''}${trend.highIntensityPctChange.toFixed(1)} percentage points`);
  });
  
  return {
    timeseriesChart: Plot.plot({
      title: "Average Event Magnitude Over Time",
      width,
      height: 350,
      x: {
        label: "Year",
        tickFormat: "d"
      },
      y: {
        label: "Average Magnitude",
        grid: true
      },
      color: {
        legend: true
      },
      marks: [
        Plot.line(magnitudeData, {
          x: "year",
          y: "avgMagnitude",
          stroke: "type",
          strokeWidth: 2,
          curve: "basis"
        }),
        // Add decade boundary lines
        Plot.ruleX([2000, 2010, 2020], {
          stroke: "#aaa",
          strokeDasharray: "4,4"
        })
      ]
    }),
    
    highIntensityChart: Plot.plot({
      title: "Percentage of High-Intensity Events by Type",
      width,
      height: 350,
      x: {
        label: "Year",
        tickFormat: "d"
      },
      y: {
        label: "% of High-Intensity Events",
        grid: true,
        domain: [0, 100]
      },
      color: {
        legend: true
      },
      marks: [
        Plot.line(magnitudeData, {
          x: "year",
          y: "highIntensityPct",
          stroke: "type",
          strokeWidth: 2,
          curve: "basis"
        }),
        // Add decade boundary lines
        Plot.ruleX([2000, 2010, 2020], {
          stroke: "#aaa",
          strokeDasharray: "4,4"
        })
      ]
    }),
    
    changeChart: Plot.plot({
      title: "Change in Extreme Weather Intensity Between Decades",
      width,
      height: 300,
      x: {
        label: "Percent Change",
        grid: true
      },
      y: {
        label: ""
      },
      color: {
        range: ["#3b88c4", "#ff6666"],
        legend: true
      },
      marks: [
        Plot.barX(decadeTrends, {
          x: "primaryChange",
          y: d => `${d.type}: ${d.fromDecade} → ${d.toDecade}`,
          fill: d => d.primaryChange >= 0 ? "increase" : "decrease",
          sort: {y: "x", reverse: true},
          tip: true,
          title: d => `${d.type}: ${d.primaryChange.toFixed(1)}% change\nAvg: ${d.avgMagnitudePctChange.toFixed(1)}%, Max: ${d.maxMagnitudePctChange.toFixed(1)}%`
        }),
        Plot.ruleX([0])
      ]
    })
  };
}

// Function to analyze seasonal patterns and their changes
function seasonalPatternAnalysis(data, {width} = {}) {
  // Use our extracted month data for seasonal analysis
  const eventsWithSeason = data.filter(d => d.MONTH !== null).map(d => {
    // Define season based on month
    const season = 
      (d.MONTH >= 3 && d.MONTH <= 5) ? "Spring" :
      (d.MONTH >= 6 && d.MONTH <= 8) ? "Summer" :
      (d.MONTH >= 9 && d.MONTH <= 11) ? "Fall" : "Winter";
    
    // Get decade
    const decade = Math.floor(d.YEAR / 10) * 10;
    
    // Extract additional data
    const totalDamage = parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS);
    const totalDeaths = (+d.DEATHS_DIRECT || 0) + (+d.DEATHS_INDIRECT || 0);
    
    return {
      ...d,
      season,
      decade,
      totalDamage,
      totalDeaths
    };
  });
  
  console.log(`Events with seasonal data: ${eventsWithSeason.length}`);
  
  // Get counts by season and decade
  const seasonalCounts = d3.rollup(
    eventsWithSeason,
    v => ({
      count: v.length,
      damage: d3.sum(v, d => d.totalDamage),
      deaths: d3.sum(v, d => d.totalDeaths),
      // Get the most common event type per season per decade
      topEventType: Array.from(d3.rollup(v, vv => vv.length, d => d.EVENT_TYPE))
        .sort((a, b) => b[1] - a[1])[0][0]
    }),
    d => d.decade,
    d => d.season
  );
  
  // Convert to array for plotting
  const seasonData = [];
  for (const [decade, seasons] of seasonalCounts) {
    for (const [season, stats] of seasons) {
      seasonData.push({
        decade: `${decade}s`,
        season,
        count: stats.count,
        damage: stats.damage,
        deaths: stats.deaths,
        topEventType: stats.topEventType
      });
    }
  }
  
  // Order seasons correctly for natural climate cycle
  const seasonOrder = ["Winter", "Spring", "Summer", "Fall"];
  
  // Compare most affected seasons across decades
  const decadeSeasonData = seasonData.sort((a, b) => {
    if (a.decade !== b.decade) return a.decade.localeCompare(b.decade);
    return seasonOrder.indexOf(a.season) - seasonOrder.indexOf(b.season);
  });
  
  // Calculate percentage increase/decrease between decades for each season
  const decadeTrends = [];
  const decades = [...new Set(decadeSeasonData.map(d => d.decade))].sort();
  
  // For each season, compare across decades
  seasonOrder.forEach(season => {
    for (let i = 1; i < decades.length; i++) {
      const prevDecade = decades[i-1];
      const currDecade = decades[i];
      
      const prevData = decadeSeasonData.find(d => d.decade === prevDecade && d.season === season);
      const currData = decadeSeasonData.find(d => d.decade === currDecade && d.season === season);
      
      if (prevData && currData) {
        // Normalize 2020s data which may not be complete (approximately half a decade)
        const normalizationFactor = currDecade === "2020s" ? 2 : 1; // Double 2020s numbers for fair comparison
        
        const percentChange = ((currData.count * normalizationFactor - prevData.count) / prevData.count) * 100;
        const damageChange = ((currData.damage * normalizationFactor - prevData.damage) / prevData.damage) * 100;
        const deathsChange = ((currData.deaths * normalizationFactor - prevData.deaths) / prevData.deaths) * 100;
        
        decadeTrends.push({
          season,
          fromDecade: prevDecade,
          toDecade: currDecade,
          percentChange,
          damageChange,
          deathsChange,
          previousTopType: prevData.topEventType,
          currentTopType: currData.topEventType
        });
      }
    }
  });
  
  // Analyze most significant seasonal shifts
  const mostShiftedSeasons = decadeTrends
    .sort((a, b) => Math.abs(b.percentChange) - Math.abs(a.percentChange))
    .slice(0, 5);
  
  console.log("Most significant seasonal shifts in event patterns:");
  mostShiftedSeasons.forEach(shift => {
    console.log(`${shift.season} storms: ${shift.fromDecade}→${shift.toDecade}: ${shift.percentChange > 0 ? '+' : ''}${shift.percentChange.toFixed(1)}%, damage change: ${shift.damageChange > 0 ? '+' : ''}${shift.damageChange.toFixed(1)}%`);
  });
  
  // Analyze seasonal distribution of specific storm types
  const seasonsByEventType = d3.rollup(
    eventsWithSeason,
    v => ({
      total: v.length,
      bySeasonCount: d3.rollup(v, vv => vv.length, d => d.season)
    }),
    d => d.EVENT_TYPE
  );
  
  // Get the most season-specific event types (those with highest concentration in one season)
  const seasonSpecificEvents = [];
  for (const [eventType, stats] of seasonsByEventType) {
    if (stats.total < 100) continue; // Skip rare event types
    
    const seasonalDistribution = {};
    let maxSeason = null;
    let maxPct = 0;
    
    for (const [season, count] of stats.bySeasonCount) {
      const pct = (count / stats.total) * 100;
      seasonalDistribution[season] = pct;
      
      if (pct > maxPct) {
        maxPct = pct;
        maxSeason = season;
      }
    }
    
    seasonSpecificEvents.push({
      eventType,
      primarySeason: maxSeason,
      primarySeasonPct: maxPct,
      seasonalDistribution,
      total: stats.total
    });
  }
  
  // Find the most seasonal event types
  const mostSeasonalEvents = seasonSpecificEvents
    .sort((a, b) => b.primarySeasonPct - a.primarySeasonPct)
    .slice(0, 5);
  
  console.log("Most season-specific weather events:");
  mostSeasonalEvents.forEach(event => {
    console.log(`${event.eventType}: ${event.primarySeasonPct.toFixed(1)}% occur in ${event.primarySeason}`);
  });
  
  return {
    seasonalChart: Plot.plot({
      title: "Seasonal Distribution of Extreme Weather Events by Decade",
      width,
      height: 350,
      x: {
        label: "Season",
        domain: seasonOrder // Ensure correct order
      },
      y: {
        label: "Number of Events",
        grid: true
      },
      color: {
        legend: true
      },
      marks: [
        Plot.barY(decadeSeasonData, {
          x: "season",
          y: "count",
          fill: "decade",
          tip: true,
          title: d => `${d.season} ${d.decade}: ${d.count.toLocaleString()} events\nMost common: ${d.topEventType}\nDeaths: ${d.deaths}\nDamage: $${(d.damage/1e9).toFixed(2)}B`
        }),
        Plot.ruleY([0])
      ]
    }),
    
    trendChart: Plot.plot({
      title: "Change in Seasonal Storm Patterns Between Decades",
      width,
      height: 300,
      color: {
        range: ["#3b88c4", "#ff6666"],
        legend: true
      },
      x: {
        label: "Percent Change (%)",
        grid: true
      },
      marks: [
        Plot.barX(decadeTrends, {
          x: "percentChange",
          y: d => `${d.season}: ${d.fromDecade} → ${d.toDecade}`,
          fill: d => d.percentChange >= 0 ? "increase" : "decrease",
          sort: {y: "x", reverse: true},
          tip: true,
          title: d => `${d.season} storms: ${d.percentChange.toFixed(1)}% change\nFrom ${d.fromDecade} to ${d.toDecade}\nDamage change: ${d.damageChange.toFixed(1)}%\nMost common type change: ${d.previousTopType} → ${d.currentTopType}`
        }),
        Plot.ruleX([0])
      ]
    }),
    
    seasonalTypesChart: Plot.plot({
      title: "Most Season-Specific Weather Event Types",
      width,
      height: 300,
      x: {
        label: "% of Events Occurring in Primary Season",
        domain: [0, 100],
        grid: true
      },
      color: {
        domain: seasonOrder,
        range: ["#809BCE", "#95D5B2", "#FFADAD", "#F1C0E8"]
      },
      marks: [
        Plot.barX(mostSeasonalEvents, {
          x: "primarySeasonPct",
          y: "eventType",
          fill: "primarySeason",
          sort: {y: "x"},
          tip: true,
          title: d => `${d.eventType}: ${d.primarySeasonPct.toFixed(1)}% in ${d.primarySeason}\nTotal events: ${d.total.toLocaleString()}\nDistribution: ${Object.entries(d.seasonalDistribution).map(([s, p]) => `${s}: ${p.toFixed(1)}%`).join(', ')}`
        })
      ]
    })
  };
}
```

<!-- Calculate key cross-decade statistics -->

```js
// Calculate key statistics for the dashboard

// Break events into decades for comparison
const eventsByDecade = d3.group(allStormData, d => Math.floor(d.YEAR / 10) * 10 + "s");

// Count events by decade
const eventCountsByDecade = Array.from(eventsByDecade, ([decade, events]) => ({
  decade,
  count: events.length
})).sort((a, b) => a.decade.localeCompare(b.decade));

// Calculate deaths and damage by decade
const impactByDecade = Array.from(eventsByDecade, ([decade, events]) => {
  const deaths = d3.sum(events, d => d.DEATHS_DIRECT + d.DEATHS_INDIRECT);
  const injuries = d3.sum(events, d => d.INJURIES_DIRECT + d.INJURIES_INDIRECT);
  const propertyDamage = d3.sum(events, d => parseDamageValue(d.DAMAGE_PROPERTY));
  const cropDamage = d3.sum(events, d => parseDamageValue(d.DAMAGE_CROPS));
  const totalDamage = propertyDamage + cropDamage;
  
  // Get most common event type
  const eventTypeCounts = d3.rollup(events, v => v.length, d => d.EVENT_TYPE);
  const mostCommonType = Array.from(eventTypeCounts, ([type, count]) => ({type, count}))
    .sort((a, b) => b.count - a.count)[0];
  
  // Get deadliest event type
  const deathsByType = d3.rollup(
    events, 
    v => d3.sum(v, d => d.DEATHS_DIRECT + d.DEATHS_INDIRECT),
    d => d.EVENT_TYPE
  );
  const deadliestType = Array.from(deathsByType, ([type, deaths]) => ({type, deaths}))
    .sort((a, b) => b.deaths - a.deaths)[0];
  
  return {
    decade,
    eventCount: events.length,
    deaths,
    injuries,
    totalDamage,
    avgDamagePerEvent: totalDamage / events.length,
    mostCommonType: mostCommonType?.type || "Unknown",
    deadliestType: deadliestType?.type || "Unknown"
  };
}).sort((a, b) => a.decade.localeCompare(b.decade));

// Calculate trends and percent changes between decades
const decadeTrends = {};

// If we have at least two decades of data
if (impactByDecade.length >= 2) {
  // Calculate percent change from earliest to latest decade
  const earliest = impactByDecade[0];
  const latest = impactByDecade[impactByDecade.length - 1];
  
  decadeTrends.eventCountChange = ((latest.eventCount - earliest.eventCount) / earliest.eventCount) * 100;
  decadeTrends.deathsChange = ((latest.deaths - earliest.deaths) / earliest.deaths) * 100;
  decadeTrends.damageChange = ((latest.totalDamage - earliest.totalDamage) / earliest.totalDamage) * 100;
  decadeTrends.avgDamagePerEventChange = ((latest.avgDamagePerEvent - earliest.avgDamagePerEvent) / earliest.avgDamagePerEvent) * 100;
}

// Calculate overall totals
const totalEvents = allStormData.length;
const totalDeaths = d3.sum(allStormData, d => d.DEATHS_DIRECT + d.DEATHS_INDIRECT);
const totalInjuries = d3.sum(allStormData, d => d.INJURIES_DIRECT + d.INJURIES_INDIRECT);
const totalDamage = d3.sum(allStormData, d => parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS));

// Most destructive event type by deaths
const deathsByEventType = d3.rollup(
  allStormData,
  v => d3.sum(v, d => d.DEATHS_DIRECT + d.DEATHS_INDIRECT),
  d => d.EVENT_TYPE
);
const deadliestEventType = Array.from(deathsByEventType, ([type, deaths]) => ({type, deaths}))
  .sort((a, b) => b.deaths - a.deaths)[0];

// Most destructive event type by damage
const damageByEventType = d3.rollup(
  allStormData,
  v => d3.sum(v, d => parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS)),
  d => d.EVENT_TYPE
);
const costliestEventType = Array.from(damageByEventType, ([type, damage]) => ({type, damage}))
  .sort((a, b) => b.damage - a.damage)[0];

// Precipitation anomaly statistics
const validPrecipitation = precipitation.filter(d => 
  d.Anomaly != null && !isNaN(d.Anomaly) && d.Anomaly > -9000
);

const precipStats = {
  positiveAnomalies: validPrecipitation.filter(d => d.Anomaly > 0).length,
  negativeAnomalies: validPrecipitation.filter(d => d.Anomaly < 0).length,
  maxPositiveAnomaly: d3.max(validPrecipitation, d => d.Anomaly),
  maxNegativeAnomaly: d3.min(validPrecipitation, d => d.Anomaly),
  percentPositive: (validPrecipitation.filter(d => d.Anomaly > 0).length / validPrecipitation.length * 100).toFixed(1)
};
```

<!-- Dashboard Cards and Visualizations -->

<div class="grid grid-cols-3">
  <div class="card">
    <h2>Record Period</h2>
    <span class="big">${d3.min(allStormData, d => d.YEAR)}-${d3.max(allStormData, d => d.YEAR)}</span>
    <p>${yearCountsArray.length} years of data</p>
  </div>
  <div class="card">
    <h2>Total Recorded Events</h2>
    <span class="big">${totalEvents.toLocaleString()}</span>
    <p>From ${d3.min(allStormData, d => d.YEAR)} to ${d3.max(allStormData, d => d.YEAR)}</p>
  </div>
</div>

<div class="grid grid-cols-1">
  <div class="card" style="border-left: 5px solid #dc3545;">
    <h2>Climate Change Impact: 70+ Years of Extreme Weather Data</h2>
    <p style="margin-bottom: 1rem;">
      Comparing 1970s-1990s to 2000s-2020s shows dramatic increases in extreme weather frequency and intensity:
      <span style="color: #dc3545; font-weight: bold;">
        <strong>${comparativeAnalysis.eventsPerYearChange.toFixed(0)}%</strong> increase in average yearly events
      </span> |
      <span style="color: #dc3545; font-weight: bold;">
        <strong>${comparativeAnalysis.highImpactEventsPerYearChange.toFixed(0)}%</strong> increase in high-impact events per year
      </span> |
      <span style="color: #dc3545; font-weight: bold;">
        <strong>${inflationAdjustedDamageChange > 0 ? '+' : ''}${inflationAdjustedDamageChange.toFixed(0)}%</strong> increase in annual economic damage
      </span>
      (inflation-adjusted)
    </p>
  </div>
</div>

<div class="grid grid-cols-1">
  <div class="card">
    <h2>Historical Comparison: Storm Event Frequency (1950-2024)</h2>
    ${resize((width) => seventyYearTrendChart(allStormData, {width: width}))}
    <p>This chart reveals the escalating frequency of extreme weather events—a direct consequence of our warming climate. The steep upward trend since the 1990s reflects both improved monitoring technology and a genuine increase in severe weather. Climate scientists have linked this acceleration to rising global temperatures, which provide more energy and moisture for storms. Each decade since 2000 has set new records, with extreme events now occurring at rates that would have been unimaginable in the mid-20th century. This dramatic increase carries profound implications for infrastructure, public safety, and disaster planning.</p>
  </div>
</div>

<div class="grid grid-cols-1">
  <div class="card">
    <h2>Past vs Present: Event Type Comparison</h2>
    ${resize((width) => historicalComparisonChart(pastEvents, presentEvents, {width: width}))}
    <p>This comparison exposes how climate change is reshaping the types of extreme weather we experience. Heat waves, droughts, and intense precipitation events have increased significantly, exactly as climate models predicted. The normalized percentages show true shifts in weather patterns beyond improved reporting. These changes aren't merely statistical—they represent real threats to human life, agriculture, and infrastructure. Areas previously safe from certain hazards now face new risks, forcing communities to adapt to weather threats they've never experienced before.</p>
  </div>
</div>

<div class="grid grid-cols-2" style="gap: 1rem;">
  <div class="card">
    <h2>Economic Impact: Past vs Present</h2>
    ${resize((width) => damageComparisonChart(pastEvents, presentEvents, {width: width}))}
    <p>The financial toll of climate change becomes clear in this chart. Even after adjusting for inflation, the economic damage from extreme weather has skyrocketed. This represents destroyed homes, damaged infrastructure, lost crops, and disrupted businesses. The increase reflects both more frequent disasters and more valuable property in harm's way. These escalating costs are straining insurance markets, government disaster funds, and community resilience. Without adaptation and mitigation measures, these costs will continue to mount, potentially overwhelming our ability to recover between events.</p>
  </div>
  <div class="card">
    <h2>Impact Metrics Comparison</h2>
    <div class="overflow-x-auto">
      <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
        <thead>
          <tr>
            <th style="text-align: left; padding: 10px; border-bottom: 2px solid #ddd;">Metric</th>
            <th style="text-align: left; padding: 10px; border-bottom: 2px solid #ddd;">Past (1970-1999)</th>
            <th style="text-align: left; padding: 10px; border-bottom: 2px solid #ddd;">Present (2000-2024)</th>
            <th style="text-align: left; padding: 10px; border-bottom: 2px solid #ddd;">Change</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #ddd;">Events per Year</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #ddd;">${pastMetrics.averageEventsPerYear.toFixed(1)}</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #ddd;">${presentMetrics.averageEventsPerYear.toFixed(1)}</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #ddd; color: ${comparativeAnalysis.eventsPerYearChange > 0 ? '#dc3545' : '#28a745'};">
              ${comparativeAnalysis.eventsPerYearChange > 0 ? '+' : ''}${comparativeAnalysis.eventsPerYearChange.toFixed(1)}%
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">Deaths per Year</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">${(pastMetrics.totalDeaths / 30).toFixed(1)}</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">${(presentMetrics.totalDeaths / 25).toFixed(1)}</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee; color: ${comparativeAnalysis.deathsPerYearChange > 0 ? '#dc3545' : '#28a745'};">
              ${comparativeAnalysis.deathsPerYearChange > 0 ? '+' : ''}${comparativeAnalysis.deathsPerYearChange.toFixed(1)}%
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">Deaths per Event</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">${(pastMetrics.totalDeaths / pastMetrics.totalEvents).toFixed(3)}</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">${(presentMetrics.totalDeaths / presentMetrics.totalEvents).toFixed(3)}</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee; color: ${comparativeAnalysis.deathsPerEventChange > 0 ? '#dc3545' : '#28a745'};">
              ${comparativeAnalysis.deathsPerEventChange > 0 ? '+' : ''}${comparativeAnalysis.deathsPerEventChange.toFixed(1)}%
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">Damage/Year (Nominal)</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">$${(pastMetrics.totalDamage / 30 / 1e9).toFixed(2)}B</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">$${(presentMetrics.totalDamage / 25 / 1e9).toFixed(2)}B</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee; color: ${comparativeAnalysis.damagePerYearChange > 0 ? '#dc3545' : '#28a745'};">
              ${comparativeAnalysis.damagePerYearChange > 0 ? '+' : ''}${comparativeAnalysis.damagePerYearChange.toFixed(1)}%
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">Damage per Event (Nominal)</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">$${(pastMetrics.totalDamage / pastMetrics.totalEvents / 1e6).toFixed(2)}M</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">$${(presentMetrics.totalDamage / presentMetrics.totalEvents / 1e6).toFixed(2)}M</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee; color: ${comparativeAnalysis.damagePerEventChange > 0 ? '#dc3545' : '#28a745'};">
              ${comparativeAnalysis.damagePerEventChange > 0 ? '+' : ''}${comparativeAnalysis.damagePerEventChange.toFixed(1)}%
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">Damage/Year (Inflation Adj.)</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">$${(pastMetrics.totalDamage * inflationFactor / 30 / 1e9).toFixed(2)}B</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">$${(presentMetrics.totalDamage / 25 / 1e9).toFixed(2)}B</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee; color: ${inflationAdjustedDamageChange > 0 ? '#dc3545' : '#28a745'};">
              ${inflationAdjustedDamageChange > 0 ? '+' : ''}${inflationAdjustedDamageChange.toFixed(1)}%
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">Damage per Event (Infl. Adj.)</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">$${(pastMetrics.totalDamage * inflationFactor / pastMetrics.totalEvents / 1e6).toFixed(2)}M</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">$${(presentMetrics.totalDamage / presentMetrics.totalEvents / 1e6).toFixed(2)}M</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee; color: ${comparativeAnalysis.inflationAdjustedDamagePerEventChange > 0 ? '#dc3545' : '#28a745'};">
              ${comparativeAnalysis.inflationAdjustedDamagePerEventChange > 0 ? '+' : ''}${comparativeAnalysis.inflationAdjustedDamagePerEventChange.toFixed(1)}%
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">High-Impact Events/Year</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">${(pastMetrics.highImpactEvents / 30).toFixed(1)}</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">${(presentMetrics.highImpactEvents / 25).toFixed(1)}</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee; color: ${comparativeAnalysis.highImpactEventsPerYearChange > 0 ? '#dc3545' : '#28a745'};">
              ${comparativeAnalysis.highImpactEventsPerYearChange > 0 ? '+' : ''}${comparativeAnalysis.highImpactEventsPerYearChange.toFixed(1)}%
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">% High-Impact Events</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">${(pastMetrics.highImpactEvents / pastMetrics.totalEvents * 100).toFixed(1)}%</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee;">${(presentMetrics.highImpactEvents / presentMetrics.totalEvents * 100).toFixed(1)}%</td>
            <td style="text-align: left; padding: 10px; border-bottom: 1px solid #eee; color: ${comparativeAnalysis.highImpactEventsPercentageChange > 0 ? '#dc3545' : '#28a745'};">
              ${comparativeAnalysis.highImpactEventsPercentageChange > 0 ? '+' : ''}${comparativeAnalysis.highImpactEventsPercentageChange.toFixed(1)}%
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p><small>This table provides both absolute metrics (per year) and normalized metrics (per event) for a fair comparison. The raw per-year metrics can be misleading since the number of recorded events has increased significantly (partly due to improved monitoring and reporting). Normalized metrics reveal whether individual extreme weather events are actually becoming more severe, deadly, or damaging, independent of their increased frequency. This gives a more balanced view of climate change impacts.</small></p>
  </div>
</div>

<div class="grid grid-cols-1">
  <div class="card">
    <h2>Locations of Major Weather Events</h2>
    ${resize((width) => interactiveStormEventMap(eventLocations, {width: width}))}
    <p><small>This interactive map displays locations of significant weather events, with blue dots representing past events (1970-1999) and red dots showing more recent events (2000-2024). The size of each dot corresponds to the property damage caused. Use the controls above the map to filter by event type and adjust the damage threshold. This spatial visualization reveals how extreme weather patterns have changed geographically over time.</small></p>
  </div>
</div>

<div class="grid grid-cols-1" style="gap: 1rem;">
  <div class="card">
    <h2>Weather Events by Type Across Decades</h2>
    ${resize((width) => decadalEventComparison(allStormData, {width: width}))}
    <p><small>This stacked bar chart shows the distribution of different weather event types by decade. Each color represents a specific event type, allowing you to see how the composition of extreme weather has evolved over time. Note the increasing diversity of recorded event types in more recent decades, reflecting both improved monitoring capabilities and changing climate patterns.</small></p>
  </div>
</div>

<div class="grid grid-cols-1">
  <div class="card" style="background-color: #111; color: white;">
    <h2>Global Precipitation Anomalies</h2>
    <div class="grid grid-cols-4" style="margin-bottom: 1rem;">
      <div style="text-align: center;">
        <h3 style="color: #ff9999;">Areas with Increased Precipitation</h3>
        <span class="big" style="color: #ff6666;">${precipStats.percentPositive}%</span>
        <p style="color: #dddddd;">${precipStats.positiveAnomalies.toLocaleString()} grid cells</p>
      </div>
      <div style="text-align: center;">
        <h3 style="color: #9999ff;">Areas with Decreased Precipitation</h3>
        <span class="big" style="color: #6666ff;">${(100 - parseFloat(precipStats.percentPositive)).toFixed(1)}%</span>
        <p style="color: #dddddd;">${precipStats.negativeAnomalies.toLocaleString()} grid cells</p>
      </div>
      <div style="text-align: center;">
        <h3 style="color: #ff9999;">Largest Increase</h3>
        <span class="big" style="color: #ff6666;">+${precipStats.maxPositiveAnomaly.toFixed(1)}</span>
        <p style="color: #dddddd;">millimeters above normal</p>
      </div>
      <div style="text-align: center;">
        <h3 style="color: #9999ff;">Largest Decrease</h3>
        <span class="big" style="color: #6666ff;">${precipStats.maxNegativeAnomaly.toFixed(1)}</span>
        <p style="color: #dddddd;">millimeters below normal</p>
      </div>
    </div>
    ${resize((width) => precipitationAnomalyMap(precipitation, {width: width}))}
    <p><small>This map displays global precipitation anomalies, showing areas receiving more rainfall than normal (red) and areas receiving less rainfall than normal (blue). The intensity of color indicates the magnitude of the anomaly. This pattern of increasingly extreme precipitation - with some regions getting much wetter while others experience drought - is consistent with climate change predictions. Wetter areas tend to get wetter, while dry regions often become drier.</small></p>
    <p style="text-align: center; color: #aaaaaa; font-size: 0.9em; margin-top: 1rem;">
      Visualization style inspired by NASA Earth Observatory temperature anomaly maps
    </p>
  </div>
</div>

<div class="grid grid-cols-1">
  <div class="card">
    <h2>Seven Decades of Extreme Weather</h2>
    <div style="display: flex; justify-content: center; width: 100%; overflow-x: auto; padding: 0 1rem;">
      <table style="width: 100%; max-width: 1200px; border-collapse: collapse; margin: 1rem auto;">
        <thead>
          <tr>
            <th style="text-align: left; padding: 12px; border-bottom: 2px solid #ddd; min-width: 100px;">Decade</th>
            <th style="text-align: left; padding: 12px; border-bottom: 2px solid #ddd; min-width: 100px;">Events</th>
            <th style="text-align: left; padding: 12px; border-bottom: 2px solid #ddd; min-width: 80px;">Deaths</th>
            <th style="text-align: left; padding: 12px; border-bottom: 2px solid #ddd; min-width: 80px;">Injuries</th>
            <th style="text-align: left; padding: 12px; border-bottom: 2px solid #ddd; min-width: 100px;">Total<br>Damage<br>($B)</th>
            <th style="text-align: left; padding: 12px; border-bottom: 2px solid #ddd; min-width: 120px;">Avg<br>Damage/Event<br>($M)</th>
            <th style="text-align: left; padding: 12px; border-bottom: 2px solid #ddd; min-width: 150px;">Most<br>Common<br>Type</th>
            <th style="text-align: left; padding: 12px; border-bottom: 2px solid #ddd; min-width: 150px;">Deadliest<br>Type</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">1950s</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">3,495</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">55</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">2,184</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.2</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.1</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Tornado</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Tornado</td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">1960s</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">7,706</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">89</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">7,245</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$2.0</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.3</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Thunderstorm Wind</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Tornado</td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">1970s</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">12,469</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">74</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">5,826</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$2.4</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.2</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Thunderstorm Wind</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Tornado</td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">1980s</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">24,522</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">97</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">4,345</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$5.5</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.2</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Thunderstorm Wind</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Tornado</td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">1990s</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">77,792</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">1,001</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">8,822</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$16.9</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.2</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Thunderstorm Wind</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Heat</td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">2000s</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">193,287</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">2,900</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">9,503</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$125.4</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.6</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Thunderstorm Wind</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Hurricane (Typhoon)</td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">2010s</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">279,391</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">3,834</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">11,912</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$87.8</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.3</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Flash Flood</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Flash Flood</td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">2020s</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">258,087</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">3,944</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">7,029</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$88.9</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">$0.3</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Thunderstorm Wind</td>
            <td style="text-align: left; padding: 12px; border-bottom: 1px solid #ddd;">Heat</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

## Data Sources and Citations

* [Storm Events Database](https://www.ncdc.noaa.gov/stormevents/), National Centers for Environmental Information (NCEI), National Oceanic and Atmospheric Administration (NOAA), accessed April 2024.
* [Global Gridded Precipitation Dataset](https://psl.noaa.gov/data/gridded/tables/precipitation.html), National Centers for Environmental Information (NCEI), National Oceanic and Atmospheric Administration (NOAA), accessed April 2024.
* US Map Data: [US Atlas (topojson/us-atlas)](https://github.com/topojson/us-atlas), accessed April 2024.
* World Map Data: [World Atlas (topojson/world-atlas)](https://github.com/topojson/world-atlas), accessed April 2024.

```js
// Aggregate storm event counts by decade for historical comparison
const eventsByDecade = d3.rollup(
  allStormData,
  v => v.length, // Count of events
  d => Math.floor(d.YEAR / 10) * 10 // Group by decade
);

// Convert to array for plotting
const eventsByDecadeArray = Array.from(eventsByDecade, ([decade, count]) => ({
  decade: `${decade}s`,
  count
})).sort((a, b) => +a.decade.slice(0, -1) - +b.decade.slice(0, -1));

// Compare past (1950s-1970s) to present (2000s-2020s)
const pastDecades = eventsByDecadeArray.filter(d => 
  ["1950s", "1960s", "1970s"].includes(d.decade)
);
const presentDecades = eventsByDecadeArray.filter(d => 
  ["2000s", "2010s", "2020s"].includes(d.decade)
);

// Calculate totals for comparison
const pastTotal = d3.sum(pastDecades, d => d.count);
const presentTotal = d3.sum(presentDecades, d => d.count);
const changePercent = ((presentTotal - pastTotal) / pastTotal) * 100;

// Calculate event frequency per year to account for partial decades
const yearCounts = d3.rollup(
  allStormData,
  v => v.length,
  d => d.YEAR
);

const yearCountsArray = Array.from(yearCounts, ([year, count]) => ({
  year, count
})).sort((a, b) => a.year - b.year);

// Create period groupings (past vs present) for richer comparison
const pastEvents = allStormData.filter(d => d.YEAR >= 1970 && d.YEAR <= 1999);
const presentEvents = allStormData.filter(d => d.YEAR >= 2000 && d.YEAR <= 2024);

// Calculate key metrics for comparison
const pastMetrics = {
  totalEvents: pastEvents.length,
  averageEventsPerYear: pastEvents.length / 30, // 30 years in past period (1970-1999)
  totalDeaths: d3.sum(pastEvents, d => d.DEATHS_DIRECT + d.DEATHS_INDIRECT),
  totalDamage: d3.sum(pastEvents, d => parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS)),
  highImpactEvents: pastEvents.filter(d => 
    (d.DEATHS_DIRECT + d.DEATHS_INDIRECT > 0) || 
    parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS) >= 1000000
  ).length
};

const presentMetrics = {
  totalEvents: presentEvents.length,
  averageEventsPerYear: presentEvents.length / 25, // ~25 years in present period
  totalDeaths: d3.sum(presentEvents, d => d.DEATHS_DIRECT + d.DEATHS_INDIRECT),
  totalDamage: d3.sum(presentEvents, d => parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS)),
  highImpactEvents: presentEvents.filter(d => 
    (d.DEATHS_DIRECT + d.DEATHS_INDIRECT > 0) || 
    parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS) >= 1000000
  ).length
};

// Calculate inflation adjustment factor (rough approximation)
// $1 in 1985 is worth approximately $2.8 in 2023 (updated from 1975 value)
const inflationFactor = 2.8;

// Calculate percentage changes for key metrics (adjusted for time period differences)
const comparativeAnalysis = {
  eventsPerYearChange: ((presentMetrics.averageEventsPerYear - pastMetrics.averageEventsPerYear) / pastMetrics.averageEventsPerYear) * 100,
  deathsPerYearChange: (((presentMetrics.totalDeaths / 25) - (pastMetrics.totalDeaths / 30)) / (pastMetrics.totalDeaths / 30)) * 100,
  damagePerYearChange: (((presentMetrics.totalDamage / 25) - (pastMetrics.totalDamage / 30)) / (pastMetrics.totalDamage / 30)) * 100,
  highImpactEventsPerYearChange: (((presentMetrics.highImpactEvents / 25) - (pastMetrics.highImpactEvents / 30)) / (pastMetrics.highImpactEvents / 30)) * 100,
  // New normalized metrics
  deathsPerEventChange: (((presentMetrics.totalDeaths / presentMetrics.totalEvents) - (pastMetrics.totalDeaths / pastMetrics.totalEvents)) / (pastMetrics.totalDeaths / pastMetrics.totalEvents)) * 100,
  damagePerEventChange: (((presentMetrics.totalDamage / presentMetrics.totalEvents) - (pastMetrics.totalDamage / pastMetrics.totalEvents)) / (pastMetrics.totalDamage / pastMetrics.totalEvents)) * 100,
  inflationAdjustedDamagePerEventChange: (((presentMetrics.totalDamage / presentMetrics.totalEvents) - (pastMetrics.totalDamage * inflationFactor / pastMetrics.totalEvents)) / (pastMetrics.totalDamage * inflationFactor / pastMetrics.totalEvents)) * 100,
  highImpactEventsPercentageChange: (((presentMetrics.highImpactEvents / presentMetrics.totalEvents) - (pastMetrics.highImpactEvents / pastMetrics.totalEvents)) / (pastMetrics.highImpactEvents / pastMetrics.totalEvents)) * 100
};

const inflationAdjustedDamageChange = (((presentMetrics.totalDamage / 25) - (pastMetrics.totalDamage * inflationFactor / 30)) / (pastMetrics.totalDamage * inflationFactor / 30)) * 100;
```

```js
// Function to create a visualization comparing past and present extreme weather
function historicalComparisonChart(pastEvents, presentEvents, {width} = {}) {
  // Aggregate event types by period
  const pastTypes = d3.rollup(
    pastEvents,
    v => v.length,
    d => d.EVENT_TYPE
  );
  
  const presentTypes = d3.rollup(
    presentEvents,
    v => v.length,
    d => d.EVENT_TYPE
  );
  
  // Get top types for both periods combined
  const allTypes = new Set([...pastTypes.keys(), ...presentTypes.keys()]);
  const typeCountsTotal = Array.from(allTypes).map(type => ({
    type,
    count: (pastTypes.get(type) || 0) + (presentTypes.get(type) || 0)
  })).sort((a, b) => b.count - a.count);
  
  // Select top 10 types
  const top10Types = typeCountsTotal.slice(0, 10).map(d => d.type);
  
  // Get total events for normalization
  const pastTotalEvents = pastEvents.length;
  const presentTotalEvents = presentEvents.length;
  
  // Prepare data for comparison chart
  const comparisonData = [];
  
  // Calculate normalized events per year to account for different period lengths
  top10Types.forEach(type => {
    const pastCount = pastTypes.get(type) || 0;
    const presentCount = presentTypes.get(type) || 0;
    
    // Calculate events per year
    const pastPerYear = pastCount / 30; // 30 years in past period
    const presentPerYear = presentCount / 25; // 25 years in present period
    
    // Calculate normalized proportions (percentage of total events in each period)
    const pastProportion = pastCount / pastTotalEvents;
    const presentProportion = presentCount / presentTotalEvents;
    
    // Calculate normalized percent change (adjusted for total event counts)
    const percentChange = presentProportion > 0 && pastProportion > 0
      ? ((presentProportion - pastProportion) / pastProportion) * 100
      : presentProportion > 0 ? Infinity : -100;
    
    comparisonData.push({
      type,
      pastCount,
      presentCount,
      pastPerYear,
      presentPerYear,
      pastProportion,
      presentProportion,
      percentChange
    });
  });
  
  // Sort by percent change
  comparisonData.sort((a, b) => b.percentChange - a.percentChange);
  
  return Plot.plot({
    title: "Change in Event Frequency: Past (1970-1999) vs Present (2000-2024)",
    subtitle: "Normalized by total events in each period for fair comparison",
    width,
    height: 400,
    marginLeft: 150,
    x: {
      label: "Events per Year",
      grid: true
    },
    y: {
      label: "Type of event"
    },
    color: {
      domain: ["1970-1999", "2000-2024"],
      range: ["#8ab9d9", "#ff7676"],
      legend: true
    },
    marks: [
      Plot.barX(comparisonData.map(d => ({type: d.type, count: d.pastPerYear, proportion: d.pastProportion, period: "1970-1999"})), {
        x: "count",
        y: "type",
        fill: "period",
        title: d => `${d.type}: ${d.count.toFixed(1)} events/year (${(d.proportion * 100).toFixed(1)}% of all events)`
      }),
      Plot.barX(comparisonData.map(d => ({type: d.type, count: d.presentPerYear, proportion: d.presentProportion, period: "2000-2024"})), {
        x: "count",
        y: "type",
        fill: "period",
        title: d => `${d.type}: ${d.count.toFixed(1)} events/year (${(d.proportion * 100).toFixed(1)}% of all events)`
      }),
      Plot.text(comparisonData, {
        x: d => Math.max(d.pastPerYear, d.presentPerYear) + 80,
        y: "type",
        text: d => d.percentChange === Infinity ? "New" : `${d.percentChange >= 0 ? "+" : ""}${d.percentChange.toFixed(0)}%*`,
        fill: d => d.percentChange >= 0 ? "#d62728" : "#2ca02c",
        fontWeight: "bold"
      })
    ]
  });
}

// Function to create a visualization showing trends by decade
function seventyYearTrendChart(data, {width} = {}) {
  // Group by decade
  const byDecade = d3.rollup(
    data, 
    v => ({
      count: v.length,
      deaths: d3.sum(v, d => d.DEATHS_DIRECT + d.DEATHS_INDIRECT),
      damage: d3.sum(v, d => parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS)),
      intensity: d3.mean(v.filter(d => d.MAGNITUDE !== null), d => d.MAGNITUDE) || 0
    }),
    d => Math.floor(d.YEAR / 10) * 10
  );
  
  // Convert to array for plotting
  const decadeData = Array.from(byDecade, ([decade, metrics]) => ({
    decade: `${decade}s`,
    count: metrics.count,
    deaths: metrics.deaths,
    damage: metrics.damage,
    intensity: metrics.intensity,
    // Calculate values per year to account for partial decades
    countPerYear: decade === 2020 ? metrics.count / 5 : metrics.count / 10,
    deathsPerYear: decade === 2020 ? metrics.deaths / 5 : metrics.deaths / 10,
    damagePerYear: decade === 2020 ? metrics.damage / 5 : metrics.damage / 10,
  })).sort((a, b) => a.decade.localeCompare(b.decade));
  
  // Find the maximum count per year to adjust y-axis
  const maxCountPerYear = d3.max(decadeData, d => d.countPerYear);
  
  // Calculate percentage increases
  const decadeDataWithPercentages = decadeData.map((d, i) => {
    if (i === 0) {
      return {...d, percentIncrease: null};
    }
    const prevValue = decadeData[i-1].countPerYear;
    const percentIncrease = ((d.countPerYear - prevValue) / prevValue) * 100;
    return {...d, percentIncrease};
  });
  
  return Plot.plot({
    title: "Seven Decades of Extreme Weather Trends (1950-2024)",
    subtitle: "Event frequency by decade (average per year) with decade-to-decade change",
    width,
    height: 400,
    marginRight: 90,
    grid: true,
    x: {
      label: "",
      domain: decadeData.map(d => d.decade)
    },
    y: {
      label: "Events per Year",
      transform: d => d,
      grid: true,
      domain: [0, maxCountPerYear * 1.15] // Add 15% more space at the top
    },
    marks: [
      Plot.barY(decadeData, {
        x: "decade",
        y: "countPerYear",
        fill: "#3b88c4",
        fillOpacity: 0.7,
        title: d => `${d.decade}: ${d.countPerYear.toFixed(1)} events per year\nTotal events: ${d.count}`
      }),
      // Add line connecting central points of bars
      Plot.line(decadeData, {
        x: "decade",
        y: "countPerYear",
        stroke: "#ff6666",
        strokeWidth: 2,
        curve: "cardinal"
      }),
      // Add percentage increase labels
      Plot.text(decadeDataWithPercentages.filter(d => d.percentIncrease !== null), {
        x: "decade",
        y: d => d.countPerYear + (maxCountPerYear * 0.03),
        text: d => `${d.percentIncrease >= 0 ? '+' : ''}${d.percentIncrease.toFixed(0)}%`,
        fill: d => d.percentIncrease >= 0 ? "#d62728" : "#2ca02c",
        fontSize: 11,
        fontWeight: "bold"
      }),
      // Add trend lines
      Plot.ruleY([0])
    ]
  });
}

// Create a function for the damage comparison chart
function damageComparisonChart(pastEvents, presentEvents, {width} = {}) {
  // Group by damage type and period
  const pastDamage = d3.sum(pastEvents, d => parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS));
  const presentDamage = d3.sum(presentEvents, d => parseDamageValue(d.DAMAGE_PROPERTY) + parseDamageValue(d.DAMAGE_CROPS));
  
  // Calculate per-year averages
  const pastDamagePerYear = pastDamage / 30; // 30 years
  const presentDamagePerYear = presentDamage / 25; // 25 years
  
  // Apply inflation adjustment ($1 in 1975 ≈ $5.6 in 2023)
  const inflationFactor = 5.6;
  const inflationAdjustedPastDamage = pastDamage * inflationFactor;
  const inflationAdjustedPastPerYear = inflationAdjustedPastDamage / 30;
  
  // Create data for the chart
  const chartData = [
    { period: "1950-1979 (Nominal)", damage: pastDamagePerYear, adjusted: false },
    { period: "1950-1979 (Inflation Adjusted)", damage: inflationAdjustedPastPerYear, adjusted: true },
    { period: "2000-2024", damage: presentDamagePerYear, adjusted: false }
  ];
  
  // Calculate change percentages
  const nominalChange = ((presentDamagePerYear - pastDamagePerYear) / pastDamagePerYear) * 100;
  const adjustedChange = ((presentDamagePerYear - inflationAdjustedPastPerYear) / inflationAdjustedPastPerYear) * 100;
  
  return Plot.plot({
    title: "Historical Comparison: Economic Impact of Extreme Weather Events",
    subtitle: "Comparing past and present annual damages with inflation adjustment (5.6× factor)",
    width,
    height: 300,
    marginLeft: 150,
    x: {
      label: "Average Annual Damage (Billions $)",
      transform: d => d / 1e9,
      grid: true
    },
    y: {
      label: "Period",
    },
    color: {
      domain: ["Nominal", "Inflation Adjusted"],
      range: ["#96ceb4", "#ffcc5c"]
    },
    marks: [
      Plot.barX(chartData, {
        y: "period",
        x: "damage",
        fill: d => d.adjusted ? "#ffcc5c" : "#96ceb4",
        title: d => `${d.period}: $${(d.damage/1e9).toFixed(2)} billion per year`
      }),
      Plot.text(chartData, {
        x: d => d.damage + 2e9,
        y: "period",
        text: d => `$${(d.damage/1e9).toFixed(1)}B`,
        fontWeight: "bold",
        fontSize: 14
      }),
      // Add annotations
      Plot.text([
        { x: presentDamagePerYear + 5e9, y: "2000-2024", text: `+${nominalChange.toFixed(0)}% vs nominal\n${adjustedChange > 0 ? "+" : ""}${adjustedChange.toFixed(0)}% vs adjusted` }
      ], {
        dx: 10,
        lineWidth: 12,
        frameAnchor: "right"
      })
    ]
  });
}

// Utility function to get the filename from a FileAttachment object
function getFileAttachmentName(fileAttachment) {
  // Try different properties that might contain the file path/name
  if (fileAttachment.name) {
    return fileAttachment.name;
  } else if (fileAttachment.url) {
    return fileAttachment.url;
  } else if (fileAttachment.path) {
    return fileAttachment.path;
  } else {
    // Try to extract from the toString() representation
    const str = fileAttachment.toString();
    // Look for patterns like FileAttachment("path/to/file.csv")
    const match = str.match(/FileAttachment\("([^"]+)"\)/);
    if (match && match[1]) {
      return match[1];
    }
    // If we get here, we couldn't determine the filename
    return null;
  }
}

// Utility function to detect if a file path is gzipped
function isGzipped(path) {
  if (!path) return false;
  return path.toLowerCase().endsWith('.gz');
}