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
    <a href="/global-temperature-dashboard" style="text-decoration: none; color: #666; font-weight: bold; border-bottom: 2px solid #666; margin-right: 1rem;">Global Temperature</a>
    <a href="/arctic-sea-ice-dashboard" style="text-decoration: none; color: #666; margin-right: 1rem;">Arctic Sea Ice</a>
    <a href="/extreme-weather-dashboard" style="text-decoration: none; color: #666; margin-right: 1rem;">Extreme Weather</a>
    <a href="/carbon-budget-dashboard" style="text-decoration: none; color: #666;">Carbon Budget</a>
  </div>
</div>

# Earth's Warming Story 🌡️

  <section aria-labelledby="intro" class="introduction">
    <p id="intro">Welcome to our journey through Earth's changing temperatures! This dashboard shows how our planet has warmed over time. Think of temperature "anomalies" as the difference between each year's temperature and what was normal during 1951-1980. When numbers are positive (shown in red), it means warmer than normal. When negative (shown in blue), it means cooler than normal.</p>
  </section>

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

## The Big Picture: Key Numbers

<div class="grid grid-cols-4">
  <div class="card">
    <h2>Data Timespan</h2>
    <span class="big">${d3.min(years)} - ${d3.max(years)}</span>
    <p><small>Our climate story spans nearly 150 years</small></p>
  </div>
  <div class="card">
    <h2>Recent Warming</h2>
    <span class="big">${recentAverage}°C</span>
    <p><small>How much warmer it's been since 2010</small></p>
  </div>
  <div class="card">
    <h2>Before Industrial Era</h2>
    <span class="big">${preindustrialAverage}°C</span>
    <p><small>Temperature difference before 1900</small></p>
  </div>
  <div class="card">
    <h2>Hottest Year</h2>
    <span class="big">${maxYear}: ${maxTemp}°C</span>
    <p><small>The record-breaking year so far</small></p>
  </div>
</div>

<p>These cards tell us an important story: Earth was relatively stable before the industrial era, but has warmed significantly in recent decades. The difference between these numbers shows the dramatic shift in our climate.</p>

<!-- Temperature anomaly timeline -->

```js
function temperatureTimeline(data, {width} = {}) {
  // Calculate the maximum absolute value for a symmetric domain
  const maxAbs = Math.max(Math.abs(minTemp), Math.abs(maxGlobalTemp));
  
  return Plot.plot({
    title: "Earth's Temperature Journey: 1880 to Today",
    width,
    height: 300,
    y: {
      grid: true, 
      label: "Temperature Change (°C)",
      domain: [-1, 1.5]
    },
    x: {
      label: "Year",
      tickFormat: d => d.toString()
    },
    color: {
      type: "diverging",
      domain: [-maxAbs, maxAbs],
      scheme: "RdBu",
      reverse: true,
      label: "Temperature Change (°C)"
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
    <p>This chart shows Earth's temperature story over time. Each dot is one year. Notice how temperatures stayed relatively stable (with ups and downs) until the 1970s. Then, something changed - temperatures began climbing steadily upward, with more and more red dots appearing. This sharp upward trend coincides with increased fossil fuel use worldwide.</p>
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
      region: "Northern Half"
    });
    
    legendData.push({
      year: d.year,
      value: d.southernHemisphere,
      region: "Southern Half"
    });
  });

  return Plot.plot({
    title: "North vs South: A Tale of Two Hemispheres",
    width,
    height: 300,
    y: {
      grid: true, 
      label: "Temperature Change (°C)",
      domain: [-0.8, 1.5]
    },
    x: {
      label: "Year",
      tickFormat: d => d.toString()
    },
    color: {
      legend: true,
      domain: ["Northern Half", "Southern Half"],
      // Use distinct colors instead of red/blue to avoid confusion with temperature
      range: ["darkorange", "steelblue"] 
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
    <p>Not all parts of Earth warm at the same rate. This chart reveals a surprising pattern: the Northern Half (orange) is warming faster than the Southern Half (blue). Why? The North has more land, which heats up quickly, while the South has more ocean, which absorbs heat more slowly. Most human activities that produce greenhouse gases also happen in the Northern Hemisphere.</p>
  </div>
</div>

## The Geography of Warming: Temperature Maps

```js
// Fetch country boundaries for the map overlay using fetch for remote URL
const countriesPromise = fetch("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(response => response.json());
const countries = await countriesPromise; // Await the promise to resolve
const land = topojson.feature(countries, countries.objects.land);
```

```js
// Function to plot the trend map
function plotTrendMap(data, valueColumn, title, {width} = {}) {
  // Calculate statistics for domain setting and debugging
  const values = data.map(d => d[valueColumn]).filter(v => !isNaN(v));
  const minVal = Math.min(...values);
  const maxVal = Math.max(...values);
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
      label: "Warming Rate (°C per decade)", 
      legend: true,
      domain: [-1, 1]
    },
    marks: [
      Plot.raster(data, {
          x: "lon",
          y: "lat",
          fill: valueColumn,
          imageRendering: "pixelated", // Use pixelated for distinct grid cells
          interpolate: "nearest",
          tip: true, 
          // title: (d) => `${d[valueColumn].toFixed(2)} °C/decade`
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
    ${resize((width) => plotTrendMap(trendData, "trend_1901_2023_C_decade", "The Long View: Temperature Changes (1901-2023)", {width}))}
    <p>This map shows Earth as a patchwork of warming. The darker the red, the faster that area has warmed over the last century. Notice how warming isn't uniform - some regions have heated up much faster than others. The Arctic (top) shows particularly intense warming, a phenomenon scientists call "Arctic amplification." When you hover over different regions, you can see exactly how quickly temperatures have changed in degrees per decade.</p>
  </div>
  <div class="card">
    ${resize((width) => plotTrendMap(trendData, "trend_1994_2023_C_decade", "The Recent Surge: Temperature Changes (1994-2023)", {width}))}
    <p>Now let's zoom in on recent decades. This map reveals how warming has accelerated since 1994. The pattern is more intense and widespread than the long-term map above. The Arctic region glows bright red, warming at alarming rates - sometimes more than 1°C per decade! This recent acceleration is why scientists are concerned about meeting climate targets set by international agreements.</p>
  </div>
</div>

## Final Considerations

Climate data tells a clear story: Earth is warming at an unprecedented rate in recorded history, primarily due to human activities. The global temperature record shows a distinct acceleration since the 1970s that coincides with increased greenhouse gas emissions.

Key takeaways from this dashboard:
- Global temperatures have risen approximately 1.2°C above pre-industrial levels
- The warming is not uniform - the Arctic, land areas, and Northern Hemisphere are warming faster
- The rate of warming has accelerated in recent decades
- The pattern of warming matches what climate models predict from greenhouse gas increases

This data underscores the urgency of reducing greenhouse gas emissions to limit future warming and its associated impacts on weather patterns, sea level rise, and ecosystems worldwide.

## Data Sources and Citations

*   GISTEMP Team, 2025: GISS Surface Temperature Analysis (GISTEMP), version 4. NASA Goddard Institute for Space Studies. Dataset accessed 2024-07-30 at [https://data.giss.nasa.gov/gistemp/](https://data.giss.nasa.gov/gistemp/).
*   Lenssen, N., G.A. Schmidt, M. Hendrickson, P. Jacobs, M. Menne, and R. Ruedy, 2024: A GISTEMPv4 observational uncertainty ensemble. *J. Geophys. Res. Atmos.*, **129**, no. 17, e2023JD040179, doi: [10.1029/2023JD040179](https://doi.org/10.1029/2023JD040179).
*   Gridded Trend Data (used for maps): Calculated from `Global_TAVG_Gridded_5.nc` (derived from GISTEMP v4).
*   Country Boundaries: [Natural Earth](https://www.naturalearthdata.com/) via [world-atlas](https://github.com/topojson/world-atlas).
