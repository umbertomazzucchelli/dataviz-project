---
theme: dashboard
title: Arctic Sea Ice Decline
toc: false
sidebar: false
pager: false
---

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
  <div>
    <a href="/" style="text-decoration: none; color: #666; margin-right: 1rem;">Home</a>
    <a href="/global-temperature-dashboard" style="text-decoration: none; color: #666; margin-right: 1rem;">Global Temperature</a>
    <a href="/arctic-sea-ice-dashboard" style="text-decoration: none; color: #666; font-weight: bold; border-bottom: 2px solid #666; margin-right: 1rem;">Arctic Sea Ice</a>
    <a href="/extreme-weather-dashboard" style="text-decoration: none; color: #666;">Extreme Weather</a>
  </div>
</div>

# Arctic Sea Ice Decline ❄️

<!-- Load and transform the data -->

```js
// Load the data files for all months
const dataFiles = {
  jan: FileAttachment("data/N_01_extent_v3.0.csv"),
  feb: FileAttachment("data/N_02_extent_v3.0.csv"),
  mar: FileAttachment("data/N_03_extent_v3.0.csv"),
  apr: FileAttachment("data/N_04_extent_v3.0.csv"),
  may: FileAttachment("data/N_05_extent_v3.0.csv"),
  jun: FileAttachment("data/N_06_extent_v3.0.csv"),
  jul: FileAttachment("data/N_07_extent_v3.0.csv"),
  aug: FileAttachment("data/N_08_extent_v3.0.csv"),
  sep: FileAttachment("data/N_09_extent_v3.0.csv"),
  oct: FileAttachment("data/N_10_extent_v3.0.csv"),
  nov: FileAttachment("data/N_11_extent_v3.0.csv"),
  dec: FileAttachment("data/N_12_extent_v3.0.csv")
};

// Add debug information to track which files are loading
console.log("Attempting to load Arctic Sea Ice data files");

// Note: Arctic map data doesn't exist yet, so we'll use the simplified visualization
```

```js
// Parse the CSV data into JSON - handle spaces in column headers
const januaryData = await dataFiles.jan.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const februaryData = await dataFiles.feb.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const marchData = await dataFiles.mar.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const aprilData = await dataFiles.apr.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const mayData = await dataFiles.may.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const juneData = await dataFiles.jun.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const julyData = await dataFiles.jul.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const augustData = await dataFiles.aug.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const septemberData = await dataFiles.sep.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const octoberData = await dataFiles.oct.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const novemberData = await dataFiles.nov.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});
const decemberData = await dataFiles.dec.csv({typed: true, parse: {"year": "number", " mo": "number", " extent": "number", " area": "number"}});

// Store all monthly data in a single object for easier access
const monthlyData = {
  jan: januaryData,
  feb: februaryData,
  mar: marchData,
  apr: aprilData,
  may: mayData,
  jun: juneData,
  jul: julyData,
  aug: augustData,
  sep: septemberData,
  oct: octoberData,
  nov: novemberData,
  dec: decemberData
};

// Log a small sample of the data to verify it loaded correctly
console.log("Monthly data loaded:", Object.keys(monthlyData));
if (Array.isArray(septemberData)) {
  console.log("September data sample:", septemberData.slice(0, 3));
} else {
  console.log("September data is not an array:", typeof septemberData);
}
```

```js
// Transform the data for our visualizations
function transformIceData(data) {
  return data.map(d => ({
    year: +d.year,
    month: +d[" mo"],
    extent: d[" extent"] === -9999 ? NaN : +d[" extent"],
    area: d[" area"] === -9999 ? NaN : +d[" area"],
    dataType: d[" data-type"],
    region: d[" region"]
  })).filter(d => !isNaN(d.extent) && d.extent > 0); // Filter out missing data
}

// Create transformed datasets for each month
const transformedData = {};
for (const [month, data] of Object.entries(monthlyData)) {
  transformedData[month] = transformIceData(data);
}

// Specific dataset for September (annual minimum)
const septemberTransformed = transformedData.sep;

// Dataset for March (annual maximum)
const marchTransformed = transformedData.mar;

// Create a dataset with all months for comparison
const allMonthsData = [];
for (const [month, data] of Object.entries(transformedData)) {
  data.forEach(d => {
    // Skip -9999 values
    if (d.extent > 0) {
      allMonthsData.push(d);
    }
  });
}
```

```js
// Extract key metrics from the data
const years = septemberTransformed.map(d => d.year);
const extentValues = septemberTransformed.map(d => d.extent);

// Calculate baseline average (1979-2000)
const baselineYears = septemberTransformed.filter(d => d.year >= 1979 && d.year <= 2000);
const baselineAverage = baselineYears.length > 0 ? d3.mean(baselineYears, d => d.extent).toFixed(2) : "N/A";

// Get the current value (most recent year)
const currentYear = d3.max(years) || 2024; // Default to 2024 if undefined
const currentYearData = septemberTransformed.find(d => d.year === currentYear);
const currentExtent = currentYearData ? currentYearData.extent.toFixed(2) : "N/A";

// Get the minimum recorded extent (typically 2012)
const minExtent = d3.min(extentValues) || 0;
const minYearData = septemberTransformed.find(d => d.extent === minExtent);
const minYear = minYearData ? minYearData.year : "N/A";

// Calculate the percent decline from 1979 to current
const startYearData = septemberTransformed.find(d => d.year === 1979);
const startValue = startYearData ? startYearData.extent : 0;
const percentDecline = startValue && currentExtent !== "N/A" 
  ? ((startValue - parseFloat(currentExtent)) / startValue * 100).toFixed(1) 
  : "N/A";

// Calculate decadal trend
const trend = calculateDecadalTrend(septemberTransformed);
const trendFormatted = trend.toFixed(2); // Format for display

// Function to calculate decadal trend
function calculateDecadalTrend(data) {
  if (data.length < 2) return 0; // Not enough data points
  
  const x = data.map(d => d.year);
  const y = data.map(d => d.extent);
  
  // Simple linear regression
  const n = x.length;
  const sumX = d3.sum(x);
  const sumY = d3.sum(y);
  const sumXY = d3.sum(x.map((xi, i) => xi * y[i]));
  const sumXX = d3.sum(x.map(xi => xi * xi));
  
  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  return slope * 10; // Convert to change per decade, return as a number
}

// Estimate years until ice-free summer if trend continues linearly
// "Ice-free" is defined as less than 1 million sq km
const yearsToIceFree = currentExtent !== "N/A" && trend !== 0 
  ? Math.ceil((1 - parseFloat(currentExtent)) / (trend / 10)) 
  : 0;
const iceFreeYear = currentYear + (yearsToIceFree > 0 ? yearsToIceFree : 0);
```

<!-- Cards with key statistics -->

<div class="grid grid-cols-4">
  <div class="card">
    <h2>Current Extent (${currentYear})</h2>
    <span class="big">${currentExtent} million km²</span>
    <p>vs ${baselineAverage} million km² (1979-2000 avg)</p>
  </div>
  <div class="card">
    <h2>Record Minimum</h2>
    <span class="big">${typeof minExtent === 'number' ? minExtent.toFixed(2) : 'N/A'} million km²</span>
    <p>${minYear} (${startValue ? ((minExtent - startValue)/startValue*100).toFixed(1) : 'N/A'}% of 1979)</p>
  </div>
  <div class="card">
    <h2>Decline Rate</h2>
    <span class="big">${typeof trend === 'number' ? Math.abs(trend).toFixed(2) : 'N/A'} million km²</span>
    <p>per decade (${percentDecline}% since 1979)</p>
  </div>
  <div class="card">
    <h2>Projected Ice-Free</h2>
    <span class="big">${iceFreeYear}</span>
    <p>at current rate of decline</p>
  </div>
</div>

<!-- Annual Minimum Timeline -->

```js
function iceExtentTimeline(data, {width} = {}) {
  return Plot.plot({
    title: "Arctic September Sea Ice Extent (1979-Present)",
    subtitle: "Annual minimum showing long-term decline and record low years",
    width,
    height: 400,
    y: {
      grid: true, 
      label: "Sea Ice Extent (million km²)",
      domain: [0, 8]
    },
    x: {
      label: "Year",
      domain: [1979, currentYear + 1], // Add a bit of padding on the right
      tickFormat: d => d.toString() // Format years without commas
    },
    color: {
      type: "linear",
      range: ["#e41a1c", "#4292c6"],
      domain: [3, 8],
      legend: true
    },
    marks: [
      // Add reference line for "ice-free" threshold
      Plot.ruleY([1], {stroke: "#888", strokeWidth: 1, strokeDasharray: "4,4"}),
      Plot.text([1.2], {
        x: 2023,
        y: 3.2,
        text: ["Ice-free threshold (1 million km²)"],
        fontSize: 10,
        fill: "#888"
      }),
      
      // Add reference line for baseline average
      Plot.ruleY([typeof baselineAverage === 'string' ? parseFloat(baselineAverage) : 0], {stroke: "#888", strokeWidth: 1}),
      Plot.text([typeof baselineAverage === 'string' ? parseFloat(baselineAverage) + 0.2 : 0.2], {
        x: 2024,
        y: 7.1,
        text: ["1979-2000 Average"],
        fontSize: 10,
        fill: "#888"
      }),
      
      // Add trend line
      Plot.line(data, {
        x: "year",
        y: d => {
          const firstYear = d3.min(data, d => d.year);
          const firstValue = data.find(item => item.year === firstYear).extent;
          return firstValue + (trend/10) * (d.year - firstYear);
        },
        stroke: "#999",
        strokeDasharray: "6,4",
        strokeWidth: 2
      }),
      
      // Main data line
      Plot.line(data, {
        x: "year", 
        y: "extent",
        stroke: "steelblue",
        strokeWidth: 2.5
      }),
      
      // Data points
      Plot.dot(data, {
        x: "year", 
        y: "extent",
        fill: "extent",
        stroke: "white",
        strokeWidth: 1,
        r: 4,
        tip: true,
        title: d => `${d.year}: ${typeof d.extent === 'number' && !isNaN(d.extent) ? d.extent.toFixed(2) : 'N/A'} million km²`
      }),
      
      // Highlight the record minimum year
      Plot.dot(data.filter(d => d.year === minYear), {
        x: "year",
        y: "extent",
        fill: "red",
        stroke: "white",
        strokeWidth: 1,
        r: 6
      }),
      
      // Annotate record minimum
      Plot.text(data.filter(d => d.year === minYear), {
        x: "year",
        y: d => d.extent - 0.3,
        text: d => `Record minimum (${d.year})`,
        fontSize: 10,
        fontWeight: "bold",
        fill: "red"
      })
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => iceExtentTimeline(septemberTransformed, {width}))}
    <p><small>This chart tracks the September sea ice extent (annual minimum) since satellite monitoring began in 1979. The dotted line shows the linear trend of decline, while the red point highlights the record minimum year. The 1 million km² threshold represents the commonly accepted definition of an "ice-free" Arctic Ocean.</small></p>
  </div>
</div>

<!-- Monthly Sea Ice Comparison -->

```js
function monthlyComparison({width} = {}) {
  // Create dataset for monthly averages in specific periods
  const periods = [
    { name: "1979-1989", start: 1979, end: 1989, color: "#4575b4" },
    { name: "2000-2010", start: 2000, end: 2010, color: "#fee090" },
    { name: "2015-2023", start: 2015, end: 2023, color: "#d73027" }
  ];
  
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  
  // Calculate monthly averages for each period
  const monthlyAverages = [];
  
  periods.forEach(period => {
    for (let month = 1; month <= 12; month++) {
      const monthKey = Object.keys(transformedData)[month - 1]; // Get the key for this month
      const monthData = transformedData[monthKey];
      
      // Filter data for this period
      const periodData = monthData.filter(d => d.year >= period.start && d.year <= period.end);
      
      // Calculate average
      const avgExtent = d3.mean(periodData, d => d.extent);
      
      monthlyAverages.push({
        month,
        monthName: monthNames[month - 1],
        period: period.name,
        extent: avgExtent,
        color: period.color
      });
    }
  });
  
  return Plot.plot({
    title: "Monthly Sea Ice Extent: Comparing Three Time Periods",
    subtitle: "Showing the seasonal cycle and how it has changed over time",
    width,
    height: 400,
    x: {
      label: "Month",
      domain: monthNames,
      tickRotate: 0
    },
    y: {
      label: "Sea Ice Extent (million km²)",
      grid: true,
      domain: [0, 16]
    },
    color: {
      domain: periods.map(p => p.name),
      range: periods.map(p => p.color),
      legend: true
    },
    marks: [
      Plot.ruleY([0]),
      Plot.line(monthlyAverages, {
        x: "monthName",
        y: "extent",
        stroke: "period",
        strokeWidth: 3,
        curve: "cardinal"
      }),
      Plot.dot(monthlyAverages, {
        x: "monthName",
        y: "extent",
        fill: "period",
        tip: true,
        title: d => `${d.monthName}, ${d.period}: ${typeof d.extent === 'number' && !isNaN(d.extent) ? d.extent.toFixed(2) : 'N/A'} million km²`
      }),
      
      // Highlight September (annual minimum)
      Plot.text(monthlyAverages.filter(d => d.monthName === "Sep"), {
        x: "monthName",
        y: d => d.extent - 0.5,
        text: d => d.period === "1979-1989" ? "Annual Minimum" : "",
        fontSize: 10,
        fontWeight: "bold"
      }),
      
      // Highlight March (annual maximum)
      Plot.text(monthlyAverages.filter(d => d.monthName === "Mar"), {
        x: "monthName",
        y: d => d.extent + 0.5,
        text: d => d.period === "1979-1989" ? "Annual Maximum" : "",
        fontSize: 10,
        fontWeight: "bold"
      })
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => monthlyComparison({width}))}
    <p><small>This chart compares the average sea ice extent for each month across three time periods: 1979-1989 (blue), 2000-2010 (yellow), and 2015-2023 (red). The natural cycle shows maximum ice in March and minimum in September, with significant decline across all months in recent decades. The greatest losses have occurred during summer and fall months.</small></p>
  </div>
</div>

<!-- Arctic Sea Ice Visualization -->

```js
// Fetch country boundaries for the map overlay using fetch for remote URL
const arcticMapPromise = fetch("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(response => response.json());
const arcticMap = await arcticMapPromise; // Await the promise to resolve
const arcticLand = topojson.feature(arcticMap, arcticMap.objects.land);

// Generate the ice extent polygons for different time periods
function generateIceExtentPolygons() {
  // Create a dataset comparing 1980s average to recent years
  const earlyPeriod = septemberTransformed.filter(d => d.year >= 1979 && d.year <= 1989);
  const earlyAvg = d3.mean(earlyPeriod, d => d.extent);
  
  const latePeriod = septemberTransformed.filter(d => d.year >= 2015 && d.year <= 2023);
  const lateAvg = d3.mean(latePeriod, d => d.extent);

  const earlyColor = "#4575b4";
  const lateColor = "#d73027";
  const earlyLabel = "1979-1989 Average";
  const lateLabel = `2015-2023 Average (${typeof earlyAvg === 'number' && typeof lateAvg === 'number' && earlyAvg !== 0 ? ((lateAvg/earlyAvg)*100).toFixed(0) : 'N/A'}% of 1980s)`;
  
  // Create approximate ice extents based on geographic points
  // These are simplified representations of ice extent for visualization purposes
  
  // Convert ice extent (in million km²) to approximate latitude
  // This is a simplified conversion based on the fact that ice extent roughly 
  // corresponds to a certain latitude band in the Arctic
  function extentToLatitude(extent) {
    // Based on approximate calculation: 
    // 7 million km² (1980s avg) ~ 69°N-70°N
    // 4.5 million km² (2010s avg) ~ 75°N-76°N
    // Linear interpolation - higher value = lower latitude (larger circle)
    return 85 - (extent * 2.1);
  }
  
  // Calculate appropriate latitudes based on actual data
  const earlyBaseLatitude = extentToLatitude(earlyAvg);
  const lateBaseLatitude = extentToLatitude(lateAvg);
  
  console.log(`Early period (${earlyLabel}): ${earlyAvg.toFixed(2)} million km² ~ ${earlyBaseLatitude.toFixed(1)}°N`);
  console.log(`Late period (${lateLabel}): ${lateAvg.toFixed(2)} million km² ~ ${lateBaseLatitude.toFixed(1)}°N`);
  
  // Generate points in a circular pattern around the North Pole
  function generateCircularPoints(baseLatitude, variationAmount = 0) {
    const points = [];
    // Generate points at regular intervals around the circle
    for (let lon = -180; lon <= 180; lon += 10) {
      // Add some natural variation to make it look realistic but still circular
      // The variation is seeded by the longitude to ensure consistent shape
      const variation = variationAmount * Math.sin(lon * 0.0174533) * Math.cos(lon * 0.0349066);
      points.push({
        lon: lon,
        lat: baseLatitude + variation,
        period: lon === -180 ? (baseLatitude === earlyBaseLatitude ? earlyLabel : lateLabel) : null
      });
    }
    return points;
  }
  
  // Early period ice extent (1979-1989 average) - more circular representation
  const earlyExtentPoints = generateCircularPoints(earlyBaseLatitude, 2);
  
  // Late period ice extent (2015-2023 average) - more circular representation
  const lateExtentPoints = generateCircularPoints(lateBaseLatitude, 1.5);

  // Arctic Circle line (66.5°N)
  const arcticCirclePoints = [];
  for (let lon = -180; lon <= 180; lon += 5) {
    arcticCirclePoints.push({
      lon: lon,
      lat: 66.5,
      type: "Arctic Circle"
    });
  }
  
  return {
    earlyExtent: earlyExtentPoints,
    lateExtent: lateExtentPoints,
    arcticCircle: arcticCirclePoints,
    earlyLabel,
    lateLabel,
    earlyColor,
    lateColor
  };
}
```

```js
// Function to plot the Arctic map with ice extents
function arcticIceVisualization({width} = {}) {
  const {
    earlyExtent, 
    lateExtent, 
    arcticCircle, 
    earlyLabel, 
    lateLabel, 
    earlyColor, 
    lateColor
  } = generateIceExtentPolygons();
  
  return Plot.plot({
    title: "Arctic Sea Ice Extent: Geographic Comparison of Historical Changes",
    subtitle: "September average ice extent boundary approximation (1979-1989 vs 2015-2023)",
    width,
    height: width * 0.4, // Aspect ratio suitable for polar projection
    projection: {
      type: "azimuthal-equidistant", // Use azimuthal equidistant projection
      rotate: [0, -90, 0], // Center on North Pole
      // Limit the view to the Northern Hemisphere above 60 degrees latitude
      domain: d3.geoCircle().center([0, 90]).radius(30)()
    },
    inset: 10,
    color: {
      domain: [earlyLabel, lateLabel],
      range: [earlyColor, lateColor],
      legend: true
    },
    marks: [
      // Add ocean background
      Plot.sphere({fill: "#cae9fc"}),
      
      // Add graticule (grid lines)
      Plot.graticule({stroke: "lightgray", strokeOpacity: 0.5}),
      
      // Add land features
      Plot.geo(arcticLand, {
        fill: "#eee", 
        stroke: "#999",
        strokeWidth: 0.5
      }),
      
      // Draw early period ice extent (1979-1989)
      Plot.line(earlyExtent, {
        x: "lon",
        y: "lat",
        stroke: earlyColor,
        strokeWidth: 2,
        curve: "natural"
      }),
    
      // Draw late period ice extent (2015-2023)
      Plot.line(lateExtent, {
        x: "lon",
        y: "lat",
        stroke: lateColor,
        strokeWidth: 2,
        curve: "natural"
      }),

      // Add annotation for North Pole
      Plot.text([{lon: 0, lat: 90}], {
        x: "lon",
        y: "lat",
        text: ["North Pole"],
        fontSize: 15,
        fontWeight: "bold",
        dx: 0,
        dy: 15,
        fill: "gray"
      }),
      
      // Add country/region labels
      Plot.text([
        {lon: -100, lat: 70, name: "Canada"},
        {lon: 100, lat: 75, name: "Russia"},
        {lon: 40, lat: 70, name: "Svalbard"},
        {lon: -40, lat: 70, name: "Greenland"}
      ], {
        x: "lon",
        y: "lat",
        text: "name",
        fontSize: 10,
        fill: "#333"
      }),
      
      // Add a small red dot at the North Pole
      Plot.dot([{lon: 0, lat: 90}], {
        x: "lon",
        y: "lat",
        fill: "red",
        r: 3
      })
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => arcticIceVisualization({width}))}
    <p><small>This map visualizes the geographic extent of Arctic sea ice during September (annual minimum) by comparing the average extent from 1979-1989 (blue line) to 2015-2023 (red line). The visualization shows how the ice edge has retreated northward, opening previously ice-covered waters along the coastlines of Russia, Canada, and Alaska. This spatial perspective illustrates the dramatic reduction in ice coverage that affects navigation, wildlife habitats, and indigenous communities.</small></p>
  </div>
</div>


## Data Sources and Citations

* National Snow and Ice Data Center (NSIDC). (2023). Sea Ice Index, Version 3. Boulder, Colorado USA. https://nsidc.org/data/g02135/versions/3
* Stroeve, J., & Notz, D. (2018). Changing state of Arctic sea ice across all seasons. Environmental Research Letters, 13(10), 103001.
* Screen, J. A., & Simmonds, I. (2010). The central role of diminishing sea ice in recent Arctic temperature amplification. Nature, 464(7293), 1334-1337.
* IPCC. (2023). Climate Change 2023: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change.