---
theme: dashboard
title: Carbon Budget Visualization
toc: false
sidebar: false
pager: false
---

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
  <div>
    <a href="/" style="text-decoration: none; color: #666; margin-right: 1rem;">Home</a>
    <a href="/global-temperature-dashboard" style="text-decoration: none; color: #666; margin-right: 1rem;">Global Temperature</a>
    <a href="/arctic-sea-ice-dashboard" style="text-decoration: none; color: #666; margin-right: 1rem;">Arctic Sea Ice</a>
    <a href="/extreme-weather-dashboard" style="text-decoration: none; color: #666; margin-right: 1rem;">Extreme Weather</a>
    <a href="/carbon-budget-dashboard" style="text-decoration: none; color: #666; font-weight: bold; border-bottom: 2px solid #666;">Carbon Budget</a>
  </div>
</div>

# Carbon Budget: Running Out of Time? 🏭

This visualization explores the global carbon budget – the amount of CO₂ we can still emit while limiting global warming to specific targets (like 1.5°C or 2°C) – and contrasts it with historical emissions from major contributing nations.

**Data Source:** EDGAR - Emissions Database for Global Atmospheric Research (CO₂ Totals by Country, 1970-2023)

<!-- Load necessary libraries and data -->
```js
const emissionsFile = FileAttachment("data/IEA_EDGAR_CO2_1970_2023/IEA_EDGAR_CO2_1970_2023_totals_by_country.csv");
```

<!-- Parse and process the data -->
```js
const emissionsDataRaw = await emissionsFile.csv({typed: true});

// --- Data Processing ---

// Identify year columns and country names
const yearColumns = emissionsDataRaw.columns.filter(d => d.startsWith("Y_"));
const years = yearColumns.map(d => parseInt(d.substring(2)));
const allCountries = emissionsDataRaw.map(d => d.Name).filter(name => name !== "World" && name !== "Int. Aviation" && name !== "Int. Shipping"); // Exclude aggregates

// Create a lookup map for faster access
const rawDataMap = new Map(emissionsDataRaw.map(d => [d.Name, d]));

// Calculate latest year's emissions (MtCO2) to find top emitters
const latestYear = d3.max(years);
const latestYearCol = `Y_${latestYear}`;
const latestEmissions = allCountries.map(country => {
  const countryData = rawDataMap.get(country);
  const value = (+countryData[latestYearCol] / 1000) || 0; // Convert kt to Mt
  return { country, value };
}).sort((a, b) => b.value - a.value);

// Select Top N countries + 'Other'
const topN = 15;
const topCountries = latestEmissions.slice(0, topN).map(d => d.country);
const otherCountries = latestEmissions.slice(topN).map(d => d.country);
const countriesToPlot = [...topCountries, "Other"];

// --- Calculate Annual Global Emissions (All Countries) ---
const annualGlobalEmissions = years.map(year => {
  const yearCol = `Y_${year}`;
  let totalYearlyMt = 0;
  allCountries.forEach(country => {
    const countryData = rawDataMap.get(country);
    totalYearlyMt += (+countryData[yearCol] / 1000) || 0; // kt to Mt
  });
  return { year: year, value: totalYearlyMt };
});

// --- Calculate Cumulative Global Emissions (GtCO2) ---
let cumulativeSumGt = 0;
const cumulativeGlobalData = annualGlobalEmissions.map(d => {
  cumulativeSumGt += d.value / 1000; // Mt to Gt
  return { year: d.year, value: cumulativeSumGt };
});

// Calculate historical emissions up to end of 2019
const historicalEmissions2019 = cumulativeGlobalData.find(d => d.year === 2019)?.value || 0;
console.log(`Historical Emissions (1970-2019): ${historicalEmissions2019.toFixed(1)} GtCO₂`);

// Transform data into long format [{year, country, value}, ...] for Stacked Area Plot
const finalDataForPlot = [];
years.forEach(year => {
  const yearCol = `Y_${year}`;
  let otherSum = 0;
  
  // Sum emissions for 'Other' countries
  otherCountries.forEach(country => {
    const countryData = rawDataMap.get(country);
    otherSum += (+countryData[yearCol] / 1000) || 0;
  });
  
  // Add data for top countries
  topCountries.forEach(country => {
    const countryData = rawDataMap.get(country);
    finalDataForPlot.push({
      year: year,
      country: country,
      value: (+countryData[yearCol] / 1000) || 0
    });
  });
  
  // Add aggregated 'Other' data
  finalDataForPlot.push({
    year: year,
    country: "Other",
    value: otherSum
  });
});

// For debugging: Log the results
console.log(`Top ${topN} countries:`, topCountries);
console.log("Final Data for Plot (first few rows):", finalDataForPlot.filter(d => d.year === years[0])); // Show data for the first year
console.log("Cumulative Global Data (first few rows):", cumulativeGlobalData.slice(0, 5));

// --- Carbon Budget Data (from IPCC AR6, starting Jan 2020) ---
const remainingBudgets = {
  "1.5C": { 50: 500, 67: 400, 83: 300 }, // GtCO2
  "2.0C": { 50: 1350, 67: 1150, 83: 900 }  // GtCO2
};

// Create a function to calculate cumulative emissions for specific countries
function calculateCumulativeEmissions(countryName) {
  const countryYearlyData = finalDataForPlot.filter(d => d.country === countryName);
  let cumulativeSum = 0;
  return years.map(year => {
    const yearData = countryYearlyData.find(d => d.year === year);
    cumulativeSum += (yearData?.value || 0) / 1000; // Convert Mt to Gt
    return { year, value: cumulativeSum };
  });
}

// --- End Data Processing ---
```

## Carbon Budget Visualization

```js
// Create a function for the stacked area chart of annual emissions
function annualEmissionsChart({width, highlight = null} = {}) {
  return Plot.plot({
    subtitle: `Top ${topN} Countries + Other (1970-${d3.max(years)})`,
    width,
    height: 450,
    x: {
      label: "Year",
      tickFormat: d => d.toString()
    },
    y: {
      label: "Annual Emissions (MtCO₂)",
      grid: true
    },
    color: {
      domain: countriesToPlot,
      scheme: "Spectral",  // Changed from tableau10 to Spectral for better accessibility
      legend: true
    },
    marks: [
      Plot.areaY(finalDataForPlot, {
        x: "year",
        y: "value",
        fill: "country",
        order: "sum",
        reverse: true,
        tip: {
          format: { 
            year: d => d.toString(),
            country: true, 
            value: (d) => `${d.toFixed(1)} MtCO₂` 
          },
          style: {
            fontSize: "14px",
            padding: "8px 12px",
            backgroundColor: "rgba(255, 255, 255, 0.95)",
            boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
            borderRadius: "4px"
          }
        },
        style: d => ({
          fillOpacity: highlight === null || d.country === highlight ? 0.8 : 0.2
        })
      }),
      Plot.ruleY([0])
    ]
  });
}
```

```js
// Create an interactive budget visualization with selectors
function carbonBudgetChart({width} = {}) {
  // DOM element for the container
  const container = document.createElement("div");
  container.className = "budget-chart-container";
  
  // Create controls
  const controlsDiv = document.createElement("div");
  controlsDiv.className = "budget-controls";
  controlsDiv.style.margin = "0 0 1em 0";
  controlsDiv.style.display = "flex";
  controlsDiv.style.gap = "2em";
  
  // Temperature target control
  const targetDiv = document.createElement("div");
  targetDiv.innerHTML = `
    <label style="display: block; margin-bottom: 0.5em; font-weight: bold;">Temperature Target</label>
    <div style="display: flex; gap: 0.5em;">
      <input type="radio" id="target-1-5c" name="temp-target" value="1.5C" checked>
      <label for="target-1-5c">1.5°C</label>
      <input type="radio" id="target-2-0c" name="temp-target" value="2.0C">
      <label for="target-2-0c">2.0°C</label>
    </div>
  `;
  
  // Probability control
  const probDiv = document.createElement("div");
  probDiv.innerHTML = `
    <label style="display: block; margin-bottom: 0.5em; font-weight: bold;">Probability</label>
    <select id="probability-select" style="padding: 0.3em; border-radius: 4px;">
      <option value="50">50% chance</option>
      <option value="67" selected>67% chance</option>
      <option value="83">83% chance</option>
    </select>
  `;
  
  // Country highlight control
  const highlightDiv = document.createElement("div");
  highlightDiv.innerHTML = `
    <label style="display: block; margin-bottom: 0.5em; font-weight: bold;">Highlight Country</label>
    <select id="country-select" style="padding: 0.3em; border-radius: 4px;">
      <option value="">None</option>
      ${countriesToPlot.map(country => `<option value="${country}">${country}</option>`).join('')}
    </select>
  `;
  
  // Add controls to container
  controlsDiv.appendChild(targetDiv);
  controlsDiv.appendChild(probDiv);
  controlsDiv.appendChild(highlightDiv);
  container.appendChild(controlsDiv);
  
  // Create div for the chart
  const chartDiv = document.createElement("div");
  chartDiv.id = "budget-chart-container";
  chartDiv.style.minHeight = "500px";
  container.appendChild(chartDiv);
  
  // Chart state
  const state = {
    temperatureTarget: "1.5C",
    probabilityLevel: 67,
    highlight: null
  };
  
  // Function to update the chart
  function updateChart() {
    const selectedRemainingBudget = remainingBudgets[state.temperatureTarget]?.[state.probabilityLevel] ?? 0;
    const selectedTotalBudget = historicalEmissions2019 + selectedRemainingBudget;
    
    const marks = [
      Plot.lineY(cumulativeGlobalData, {
        x: "year",
        y: "value",
        stroke: "#2b5d7d",  // Changed from black to a deep blue
        strokeWidth: 2.5,
      }),
      Plot.ruleY([selectedTotalBudget], {
        stroke: "#d95f02",  // Changed from red to a more accessible orange
        strokeWidth: 2,
        strokeDasharray: "6,4",
      }),
      // Add point to highlight current emissions
      Plot.dot(cumulativeGlobalData.filter(d => d.year === d3.max(years)), {
        x: "year",
        y: "value",
        r: 6,
        fill: "#2b5d7d",  // Match line color
        stroke: "white",
        strokeWidth: 1.5,
        title: d => `Current (${d.year}): ${d.value.toFixed(1)} GtCO₂`
      }),
      // Add point to highlight remaining budget threshold
      Plot.dot([{year: 2050, value: selectedTotalBudget}], {
        x: "year",
        y: "value", 
        r: 0,
        fill: "#d95f02",  // Match budget line color
        stroke: "white",
        strokeWidth: 1.5,
        title: d => `Budget: ${d.value.toFixed(1)} GtCO₂ (${state.temperatureTarget} @ ${state.probabilityLevel}%)`
      }),
      // Add text labels for budget limit and current emissions
      Plot.text([{year: 2035, value: selectedTotalBudget}], {
        x: "year",
        y: "value",
        dy: -15,
        text: d => `Budget limit: ${selectedTotalBudget.toFixed(1)} GtCO₂ (${state.temperatureTarget} @ ${state.probabilityLevel}%)`,
        fill: "#d95f02",
        fontWeight: "bold",
        fontSize: 14
      }),
      Plot.text(cumulativeGlobalData.filter(d => d.year === d3.max(years)), {
        x: "year",
        y: "value",
        dy: -15,
        text: d => `Current (${d.year}): ${d.value.toFixed(1)} GtCO₂`,
        fill: "#2b5d7d",
        fontWeight: "bold",
        fontSize: 14
      })
    ];
    
    // Add highlighted country's cumulative emissions if one is selected
    if (state.highlight) {
      const countryData = calculateCumulativeEmissions(state.highlight);
      marks.push(
        Plot.lineY(countryData, {
          x: "year",
          y: "value",
          stroke: "#7570b3",  // Changed from green to a more accessible purple
          strokeWidth: 2,
          strokeDasharray: "3,3",
        }),
        Plot.dot(countryData.filter(d => d.year === d3.max(years)), {
          x: "year",
          y: "value",
          r: 6,
          fill: "#7570b3",  // Match line color
          stroke: "white",
          strokeWidth: 1.5,
          title: d => `${state.highlight} (${d.year}): ${d.value.toFixed(1)} GtCO₂`
        }),
        // Add text for highlighted country's current emissions
        Plot.text(countryData.filter(d => d.year === d3.max(years)), {
          x: "year",
          y: "value",
          dy: -15,
          text: d => `${state.highlight} (${d.year}): ${d.value.toFixed(1)} GtCO₂`,
          fill: "#7570b3",
          fontWeight: "bold",
          fontSize: 14
        })
      );
    }
    
    const chart = Plot.plot({
      subtitle: `Carbon budget shown for ${state.temperatureTarget} limit with ${state.probabilityLevel}% probability${state.highlight ? ` (Highlighting: ${state.highlight})` : ''}`, 
      width,
      height: 500,
      x: {
        label: "Year",
        tickFormat: d => d.toString()
      },
      y: {
        label: "Cumulative Global Emissions (GtCO₂)",
        grid: true
      },
      color: {
        domain: state.highlight ? ["Global Emissions", "Budget Limit", state.highlight] : ["Global Emissions", "Budget Limit"],
        range: ["#2b5d7d", "#d95f02", "#7570b3"],  // Updated color scheme
        legend: true
      },
      marks: marks
    });
    
    // Clear the chart container and append the new chart
    chartDiv.innerHTML = "";
    chartDiv.appendChild(chart);
  }
  
  // Add event listeners
  container.addEventListener("change", (event) => {
    // Temperature target change
    if (event.target.name === "temp-target") {
      state.temperatureTarget = event.target.value;
      updateChart();
    }
    
    // Probability change
    if (event.target.id === "probability-select") {
      state.probabilityLevel = +event.target.value;
      updateChart();
    }
    
    // Country highlight change 
    if (event.target.id === "country-select") {
      state.highlight = event.target.value || null;
      
      // Update both charts
      updateChart();
      
      const annualChart = annualEmissionsChart({width, highlight: state.highlight});
      const annualChartContainer = document.getElementById("annual-emissions-chart");
      if (annualChartContainer) {
        annualChartContainer.innerHTML = "";
        annualChartContainer.appendChild(annualChart);
      }
    }
  });
  
  // Initial chart render
  updateChart();
  
  return container;
}
```

<div class="grid grid-cols-1">
  <div class="card">
    <h3>Annual CO₂ Emissions by Country</h3>
    <div id="annual-emissions-chart">
      ${resize((width) => annualEmissionsChart({width}))}
    </div>
    <p>This stacked area chart shows annual CO₂ emissions by country since 1970. The top ${topN} emitting countries are shown individually, with the remaining countries aggregated as "Other". The chart reveals how global emissions have grown over time and which countries contribute most to these emissions. Use the interactive controls in the section below to highlight specific countries.</p>
  </div>
</div>

<div class="grid grid-cols-1">
  <div class="card">
    <h3>Cumulative Global CO₂ Emissions vs. Carbon Budget</h3>
    ${resize((width) => carbonBudgetChart({width}))}
    <p>This interactive visualization shows our remaining carbon budget - the amount of CO₂ we can still emit while having a chance to limit warming to specific temperature targets. You can adjust the temperature goal (1.5°C or 2.0°C) and probability level using the controls above. The steeper the line's slope, the faster we're using up our remaining budget. The highlighted country shows the contribution of individual nations to global emissions.</p>
  </div>
</div>

## Sector Breakdown by Country

<div class="grid grid-cols-1">
  <div class="card">
    <h3>Emissions by Sector for Top Emitters (${latestSectorYear})</h3>
    ${resize((width) => sectorBreakdownChart({width}))}
    <p>This chart shows emissions broken down by sector for the top emitting countries. The distribution reveals which economic activities contribute most to each country's carbon footprint. Energy production and industry typically dominate emissions profiles, though the specific mix varies by country based on their energy sources, industrial base, and development level. Understanding these sectoral differences is crucial for developing targeted climate policies that address each nation's unique emissions profile. This chart also exposes the inequality in carbon emissions responsibility: Just 15 countries produce the vast majority of global CO₂, with China and the United States far exceeding others. This uneven distribution of emissions raises critical questions about climate justice: who bears responsibility for historical emissions, who should make the deepest cuts, and how should climate action costs be shared? Nations with the largest carbon footprints face mounting pressure to lead the transition to cleaner energy systems and compensate more vulnerable countries already suffering from climate impacts they did little to cause.</p>
  </div>
</div>

## Final Considerations

The carbon budget concept provides a tangible framework for understanding how much more greenhouse gas emissions humanity can release while still having a chance to limit warming to internationally agreed temperature targets.

Key takeaways from this dashboard:
- Our remaining carbon budget is being depleted rapidly at current emission rates
- A limited number of countries account for the majority of historical emissions
- Meeting the 1.5°C target requires immediate and steep emission reductions worldwide
- Even the less ambitious 2.0°C target requires significant action within the next decade
- Past emissions have already committed us to some level of climate change

This data underscores the urgency of climate action and the need for both major emitters and developing nations to work together on mitigation strategies. While the challenge is immense, transitioning to renewable energy, improving efficiency, and implementing carbon removal technologies can help humanity stay within these critical carbon budget limits.

## Data Sources and Citations

* [Emissions Database for Global Atmospheric Research (EDGAR)](https://edgar.jrc.ec.europa.eu/)
* [International Energy Agency (IEA) CO₂ Emissions Database](https://www.iea.org/data-and-statistics/data-product/emissions-factors-2024)
* [IPCC Sixth Assessment Report (AR6) Carbon Budget Estimates](hhttps://www.ipcc-data.org/)

<!-- Load necessary libraries and data -->
```js
// Load the sector data file
const sectorDataFile = FileAttachment("data/IEA_EDGAR_CO2_1970_2023/IEA_EDGAR_CO2_1970_2023_IPCC2006.csv");
```

<!-- Parse and process the data -->
```js
const sectorDataRaw = await sectorDataFile.csv({typed: true});

// Create a lookup for sector names
const sectorNames = {
  "1.A.1.a": "Electricity & Heat",
  "1.A.1.b": "Petroleum Refining",
  "1.A.1.c": "Fuel Production",
  "1.A.2": "Manufacturing & Construction",
  "1.A.3.a": "Domestic Aviation",
  "1.A.3.b_noRES": "Road Transportation",
  "1.A.3.c": "Railways",
  "1.A.3.d": "Shipping",
  "1.A.3.e": "Other Transportation",
  "1.A.4": "Residential & Commercial",
  "1.A.5": "Other Combustion",
  "1.B.1": "Coal Mining",
  "1.B.2": "Oil & Gas",
  "2.A": "Mineral Products",
  "2.B": "Chemical Industry",
  "2.C": "Metal Production",
  "2.D": "Other Production",
  "2.G": "Other Product Use"
};

// Get sector codes
const sectorCodes = Object.keys(sectorNames);

// Create sector groups for visualization
const sectorGroups = {
  "Energy": ["1.A.1.a", "1.A.1.b", "1.A.1.c", "1.B.1", "1.B.2"],
  "Industry": ["1.A.2", "2.A", "2.B", "2.C", "2.D", "2.G"],
  "Transportation": ["1.A.3.a", "1.A.3.b_noRES", "1.A.3.c", "1.A.3.d", "1.A.3.e"],
  "Buildings": ["1.A.4"],
  "Other": ["1.A.5"]
};

// Filter out aggregates and get unique countries
const countries = [...new Set(sectorDataRaw
  .filter(d => d.fossil_bio === "fossil") // Only include fossil fuels
  .filter(d => d.Name !== "World" && d.Name !== "Int. Aviation" && d.Name !== "Int. Shipping")
  .map(d => d.Name))];

// Get the most recent year of data
const sectorYears = sectorDataRaw.columns
  .filter(col => col.startsWith("Y_"))
  .map(col => parseInt(col.substring(2)));
const latestSectorYear = Math.max(...sectorYears);
const latestSectorYearCol = `Y_${latestSectorYear}`;

// Process data by country and sector
const processedSectorData = [];

countries.forEach(country => {
  const countryData = sectorDataRaw.filter(d => d.Name === country && d.fossil_bio === "fossil");
  
  // Skip if no data
  if (countryData.length === 0) return;
  
  // Calculate total emissions for latest year
  let totalEmissions = 0;
  const sectorEmissions = {};
  
  // Initialize sector groups
  Object.keys(sectorGroups).forEach(group => {
    sectorEmissions[group] = 0;
  });
  
  // Sum emissions by sector
  countryData.forEach(row => {
    const sectorCode = row.ipcc_code_2006_for_standard_report;
    const emissions = +row[latestSectorYearCol] || 0;
    
    // Add to total
    totalEmissions += emissions;
    
    // Add to sector group
    for (const [group, codes] of Object.entries(sectorGroups)) {
      if (codes.includes(sectorCode)) {
        sectorEmissions[group] += emissions;
        break;
      }
    }
  });
  
  // Convert kt to Gt for better readability
  totalEmissions = totalEmissions / 1e6;
  Object.keys(sectorEmissions).forEach(sector => {
    sectorEmissions[sector] = sectorEmissions[sector] / 1e6;
  });
  
  processedSectorData.push({
    country,
    totalEmissions,
    sectorEmissions
  });
});

// Sort by total emissions and get top countries
const topEmittingCountries = processedSectorData
  .sort((a, b) => b.totalEmissions - a.totalEmissions)
  .slice(0, 15);

console.log("Top emitters:", topEmittingCountries);

// Prepare data for visualizations
const totalEmissionsData = topEmittingCountries.map(d => ({
  country: d.country,
  value: d.totalEmissions
}));

// Prepare sector breakdown data for visualization
const sectorEmissionsData = [];
Object.keys(sectorGroups).forEach(sector => {
  topEmittingCountries.forEach(country => {
    sectorEmissionsData.push({
      country: country.country,
      sector,
      value: country.sectorEmissions[sector]
    });
  });
});

// Prepare data for the sector TreeMap
const sectorTreemapData = {
  name: "Emissions",
  children: topEmittingCountries.map(emitter => ({
    name: emitter.country,
    value: emitter.totalEmissions,
    children: Object.entries(emitter.sectorEmissions)
      .filter(([sector, value]) => value > 0)
      .map(([sector, value]) => ({
        name: sector,
        value
      }))
  }))
};
```

```js
// Function to create the total emissions bar chart
function totalEmissionsChart({width}) {
  return Plot.plot({
    title: `Top 15 CO₂ Emitting Countries (${latestSectorYear})`,
    width,
    height: 450,
    marginLeft: 120,
    x: {
      label: "CO₂ Emissions (GtCO₂)",
      grid: true,
    },
    y: {
      label: null,
      domain: topEmittingCountries.map(d => d.country).reverse(),
      tickSize: 0,
    },
    color: {
      range: ["#2b5d7d"],
    },
    marks: [
      Plot.barX(topEmittingCountries, {
        x: "totalEmissions",
        y: "country",
        fill: "#2b5d7d",
        tip: {
          format: {
            totalEmissions: (d) => `${d.toFixed(2)} GtCO₂`
          },
          style: {
            fontSize: "14px",
            padding: "8px 12px",
            backgroundColor: "rgba(255, 255, 255, 0.95)",
            boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
            borderRadius: "4px"
          }
        }
      }),
      Plot.ruleX([0])
    ]
  });
}
```

```js
// Function to create the sector breakdown chart
function sectorBreakdownChart({width}) {
  // Create stacked bar chart for sector breakdown
  return Plot.plot({
    width,
    height: 500,
    marginLeft: 120,
    x: {
      label: "CO₂ Emissions (GtCO₂)",
      grid: true,
    },
    y: {
      label: null,
      domain: topEmittingCountries.map(d => d.country).reverse(),
      tickSize: 0,
    },
    color: {
      domain: Object.keys(sectorGroups),
      range: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
      legend: true
    },
    marks: [
      Plot.barX(sectorEmissionsData, {
        x: "value",
        y: "country",
        fill: "sector",
        tip: {
          format: {
            value: (d) => `${d.toFixed(2)} GtCO₂`
          },
          style: {
            fontSize: "14px",
            padding: "8px 12px",
            backgroundColor: "rgba(255, 255, 255, 0.95)",
            boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
            borderRadius: "4px"
          }
        }
      }),
      Plot.ruleX([0])
    ]
  });
}
```