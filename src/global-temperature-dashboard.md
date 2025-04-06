---
theme: dashboard
title: Global Temperature Anomalies
toc: false
sidebar: false
pager: false
---

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
  <div>
    <a href="/" style="text-decoration: none; color: #666; margin-right: 1rem;">Home</a>
    <a href="/arctic-sea-ice-dashboard" style="text-decoration: none; color: #666;">Arctic Sea Ice</a>
  </div>
</div>

# Global Temperature Anomalies 🌡️

<!-- Load and transform the data -->

```js
const temperatureFile = FileAttachment("data/ZonAnn.Ts+dSST.csv");
const griddedTrendFile = FileAttachment("data/gridded_trends.csv");
```

```js
// Parse the CSV data into JSON
const csvData = temperatureFile.csv();
const trendData = griddedTrendFile.csv({typed: true}); // typed: true parses numbers
```

```js
// Transform the data for our visualizations
function transformData(data) {
  return data.map(d => ({
    year: +d.Year,
    global: +d.Glob,
    northernHemisphere: +d.NHem,
    southernHemisphere: +d.SHem,
    tropics: +d["24S-24N"],
    northernExtratropics: +d["24N-90N"],
    southernExtratropics: +d["90S-24S"]
  }));
}

const temperatureData = transformData(csvData);
```

```js
// Extract key metrics from the data
const years = temperatureData.map(d => d.year);
const globalValues = temperatureData.map(d => d.global);

const recentAverage = d3.mean(temperatureData.filter(d => d.year >= 2010), d => d.global).toFixed(2);
const preindustrialAverage = d3.mean(temperatureData.filter(d => d.year < 1900), d => d.global).toFixed(2);
const maxTemp = d3.max(globalValues);
const maxYear = temperatureData.find(d => d.global === maxTemp).year;

// Find the min and max temperature for consistent color scales
const minTemp = d3.min(globalValues);
const maxGlobalTemp = d3.max(globalValues);
```

<!-- Cards with key statistics -->

<div class="grid grid-cols-4">
  <div class="card">
    <h2>Data Time Range</h2>
    <span class="big">${d3.min(years)} - ${d3.max(years)}</span>
  </div>
  <div class="card">
    <h2>Recent Global Average</h2>
    <span class="big">${recentAverage}°C</span>
  </div>
  <div class="card">
    <h2>Pre-Industrial</h2>
    <span class="big">${preindustrialAverage}°C</span>
  </div>
  <div class="card">
    <h2>Warmest Year</h2>
    <span class="big">${maxYear}: ${maxTemp}°C</span>
  </div>
</div>

<!-- Temperature anomaly timeline -->

```js
function temperatureTimeline(data, {width} = {}) {
  // Calculate the maximum absolute value for a symmetric domain
  const maxAbs = Math.max(Math.abs(minTemp), Math.abs(maxGlobalTemp));
  
  return Plot.plot({
    title: "Global Temperature Anomalies Over Time",
    width,
    height: 300,
    y: {
      grid: true, 
      label: "Temperature Anomaly (°C)",
      domain: [-1, 1.5]
    },
    x: {
      label: "Year"
    },
    color: {
      type: "diverging",
      domain: [-maxAbs, 0, maxAbs],
      scheme: "RdBu",
      reverse: true,
      label: "Temperature Anomaly (°C)"
    },
    marks: [
      Plot.ruleY([0], {stroke: "#888", strokeWidth: 1}),
      Plot.line(data, {
        x: "year", 
        y: "global",
        stroke: "global",
        z: null
      }),
      Plot.dot(data, {
        x: "year", 
        y: "global",
        fill: "global",
        r: 2,
        tip: true,
        z: null
      })
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => temperatureTimeline(temperatureData, {width}))}
  </div>
</div>

<!-- Hemisphere comparison -->

```js
function hemisphereComparison(data, {width} = {}) {
  // Create a transformed dataset with region labels
  const legendData = [];
  
  // Add points for each hemisphere
  data.forEach(d => {
    legendData.push({
      year: d.year,
      value: d.northernHemisphere,
      region: "Northern Hemisphere"
    });
    
    legendData.push({
      year: d.year,
      value: d.southernHemisphere,
      region: "Southern Hemisphere"
    });
  });

  return Plot.plot({
    title: "Northern vs Southern Hemisphere Temperature Anomalies",
    width,
    height: 300,
    y: {
      grid: true, 
      label: "Temperature Anomaly (°C)",
      domain: [-0.8, 1.5]
    },
    x: {
      label: "Year"
    },
    color: {
      legend: true,
      domain: ["Northern Hemisphere", "Southern Hemisphere"],
      range: ["red", "blue"]
    },
    marks: [
      Plot.ruleY([0], {stroke: "#888", strokeWidth: 1}),
      Plot.line(legendData, {
        x: "year", 
        y: "value",
        stroke: "region",
        strokeWidth: 2
      })
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => hemisphereComparison(temperatureData, {width}))}
  </div>
</div>

<!-- Temperature Trend Maps -->

```js
// Fetch country boundaries for the map overlay using fetch for remote URL
const countriesPromise = fetch("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(response => response.json());
const countries = await countriesPromise; // Await the promise to resolve
const land = topojson.feature(countries, countries.objects.land);
```

```js
// Function to plot the trend map
function plotTrendMap(data, valueColumn, title, {width} = {}) {
  // Determine appropriate color domain based on the period
  let colorDomain;
  
  if (valueColumn === "trend_1994_2023_C_decade") {
    // Fixed range for 1994-2023 data which has more extreme values
    colorDomain = [-1, 0, 1]; // Asymmetric to better show the warming trend
  } else {
    // For the longer-term trends (1901-2023)
    colorDomain = [-1, 0, 1];
  }

  // Calculate statistics for console debugging
  const values = data.map(d => d[valueColumn]).filter(v => !isNaN(v));
  const maxVal = Math.max(...values);
  const minVal = Math.min(...values);
  console.log(`${title} data range: ${minVal.toFixed(2)} to ${maxVal.toFixed(2)} °C/decade`);

  return Plot.plot({
    title: title,
    width,
    projection: "equal-earth",
    grid: true, // Enable grid lines
    inset: 10, // Add space around the map
    color: {
      type: "diverging",
      scheme: "RdBu",
      reverse: true,
      domain: colorDomain,
      label: "ΔT (°C/decade): ", 
      legend: true
    },
    marks: [
      Plot.raster(data, {
          x: "lon",
          y: "lat",
          fill: valueColumn,
          imageRendering: "pixelated", // Use pixelated for distinct grid cells
          interpolate: "nearest",
          tip: true, 
          title: (d) => `${d[valueColumn].toFixed(2)} °C/decade`
      }),
      Plot.graticule({stroke: "gray", strokeOpacity: 0.6, strokeDasharray: "2,2"}),
      Plot.frame(),
      Plot.geo(land, {stroke: "black", strokeWidth: 0.5, fill: "none"})
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => plotTrendMap(trendData, "trend_1901_2023_C_decade", "1901-2023", {width}))}
  </div>
  <div class="card">
    ${resize((width) => plotTrendMap(trendData, "trend_1994_2023_C_decade", "1994-2023", {width}))}
  </div>
</div>

<!-- Annual temperature distribution -->

```js
function temperatureDistribution(data, {width} = {}) {
  const decades = [];
  
  // Group data by decades
  for (let year = 1880; year <= 2020; year += 10) {
    const decadeData = data.filter(d => d.year >= year && d.year < year + 10);
    decades.push({
      decade: `${year}s`,
      min: d3.min(decadeData, d => d.global),
      q1: d3.quantile(decadeData.map(d => d.global), 0.25),
      median: d3.median(decadeData, d => d.global),
      q3: d3.quantile(decadeData.map(d => d.global), 0.75),
      max: d3.max(decadeData, d => d.global)
    });
  }
  
  // Find max absolute value among medians for a symmetric domain
  const medians = decades.map(d => d.median);
  const maxAbsMedian = Math.max(Math.abs(d3.min(medians)), Math.abs(d3.max(medians)));
  
  return Plot.plot({
    title: "Temperature Distribution by Decade",
    width,
    height: 300,
    x: {
      domain: decades.map(d => d.decade),
      label: null
    },
    y: {
      grid: true,
      label: "Temperature Anomaly (°C)",
      domain: [-0.8, 1.5]
    },
    color: {
      type: "diverging",
      domain: [-maxAbsMedian, 0, maxAbsMedian],
      scheme: "RdBu",
      reverse: true,
      label: "Temperature Anomaly (°C)"
    },
    marks: [
      Plot.ruleY([0], {stroke: "#888", strokeWidth: 1}),
      Plot.boxY(decades, {
        x: "decade",
        y1: "min",
        y2: "max",
        median: "median",
        q1: "q1",
        q3: "q3",
        fill: "median",
        z: null
      })
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => temperatureDistribution(temperatureData, {width}))}
  </div>
</div>

## Data Sources and Citations

*   GISTEMP Team, 2025: GISS Surface Temperature Analysis (GISTEMP), version 4. NASA Goddard Institute for Space Studies. Dataset accessed 2024-07-30 at [https://data.giss.nasa.gov/gistemp/](https://data.giss.nasa.gov/gistemp/).
*   Lenssen, N., G.A. Schmidt, M. Hendrickson, P. Jacobs, M. Menne, and R. Ruedy, 2024: A GISTEMPv4 observational uncertainty ensemble. *J. Geophys. Res. Atmos.*, **129**, no. 17, e2023JD040179, doi:[10.1029/2023JD040179](https://doi.org/10.1029/2023JD040179).
*   Gridded Trend Data (used for maps): Calculated from [Global_TAVG_Gridded_5.nc](https://data.giss.nasa.gov/pub/gistemp/gistemp_5x5_v1/Global_TAVG_Gridded_5.nc) (derived from GISTEMP v4).
*   Country Boundaries: [Natural Earth](https://www.naturalearthdata.com/) via [world-atlas](https://github.com/topojson/world-atlas).
