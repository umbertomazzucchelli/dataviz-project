# Visualization Reasoning for Global Temperature Dashboard

This document explains the rationale behind the visualizations used in the `global-temperature-dashboard.md` file.

## 1. Key Numbers (Cards)

*   **Purpose:** To provide a quick, high-level overview of the most important metrics derived from the temperature data. This allows users to grasp the core findings immediately.
*   **Why Cards?** Cards are excellent for displaying distinct, key performance indicators (KPIs) or summary statistics. They break down complex information into easily digestible chunks. The large font size emphasizes the values, and the accompanying text provides context.
*   **Alternatives Discarded:**
    *   **Table:** A table could show these numbers, but it wouldn't have the same visual impact or be as scannable as individual cards.
    *   **Text Paragraph:** Simply listing the numbers in a paragraph would make them harder to pick out and less engaging.

## 2. Temperature Anomaly Timeline (Line + Dot Plot)

*   **Purpose:** To show the trend of global temperature anomalies over the entire historical period (1880-present). This visualization aims to clearly illustrate the long-term warming trend, especially the acceleration in recent decades.
*   **Why Line + Dot Plot?**
    *   **Line Plot:** Effectively shows trends and continuity over time. The line connects the yearly data points, highlighting the overall pattern of change.
    *   **Dots:** Represent the discrete data for each year, allowing users to see individual annual variations and adding precision. Tooltips on the dots provide exact values on hover.
    *   **Diverging Color Scale (Red/Blue):** Intuitively maps positive anomalies (warmer) to red and negative anomalies (cooler) to blue, centered around the zero line (baseline average). This makes the shift towards warmer temperatures visually striking.
*   **Alternatives Discarded:**
    *   **Bar Chart:** While usable for time series, a bar chart might imply discrete categories rather than a continuous trend. It could also look cluttered with ~150 bars.
    *   **Area Chart:** Could obscure the zero line and make it harder to judge negative vs. positive anomalies precisely, although it would emphasize the magnitude of change.
    *   **Scatter Plot (Dots only):** Would show individual years but make the overall long-term trend less immediately obvious than the connecting line.

## 3. Hemisphere Comparison (Line Plot)

*   **Purpose:** To compare the warming trends in the Northern Hemisphere versus the Southern Hemisphere, highlighting the difference in warming rates between the two.
*   **Why Line Plot?** A multi-line plot is ideal for comparing trends of two or more series over the same time period. It clearly shows how the two hemispheres' temperature anomalies have evolved relative to each other.
*   **Color Choice:** Using distinct colors (orange and blue) unrelated to the red/blue temperature scale avoids confusion. The legend clearly identifies which line corresponds to which hemisphere.
*   **Alternatives Discarded:**
    *   **Stacked Area Chart:** Not suitable here as the goal is comparison, not showing a part-to-whole relationship. Stacking anomalies wouldn't be meaningful.
    *   **Separate Charts:** Plotting each hemisphere on a separate chart would make direct comparison much harder.
    *   **Bar Chart:** Similar drawbacks as for the main timeline – less effective at showing continuous trends and potential clutter.

## 4. Geography of Warming Maps (Raster Maps)

*   **Purpose:** To visualize the spatial distribution of warming trends across the globe, showing which areas are warming faster than others. Two maps are used: one for the long-term trend (1901-2023) and one for the recent, accelerated trend (1994-2023).
*   **Why Raster Maps?**
    *   **Geographic Representation:** Maps are the natural choice for displaying geographically distributed data.
    *   **Raster (`Plot.raster`):** Suitable for displaying gridded data where each cell has a value (temperature trend). `imageRendering: "pixelated"` ensures distinct grid cells are visible.
    *   **Diverging Color Scale (Red/Blue):** Again, effectively represents warming (red) and cooling (blue) relative to a baseline trend, allowing quick identification of hotspots like the Arctic.
    *   **Map Projection (`equal-earth`):** Chosen to provide a visually balanced representation of land areas.
    *   **Overlays:** Graticules (latitude/longitude lines) and country outlines provide geographic context.
*   **Alternatives Discarded:**
    *   **Choropleth Map (Country-based):** Would average trends over entire countries, masking significant regional variations within large nations and being dependent on potentially arbitrary political boundaries. Gridded data allows for much higher spatial resolution.
    *   **Point Map (e.g., Bubble Map):** Not suitable for showing continuous, gridded data; better for discrete locations.
    *   **Contour Map:** Could be an alternative, but raster maps with pixelated rendering clearly show the underlying grid structure of the data source.

## 5. Arctic Scorecard (Cards)

*   **Purpose:** Similar to the global temperature dashboard, these cards provide a quick summary of the most critical Arctic sea ice metrics: current extent vs. baseline, record low, rate of loss (trend), and projected first ice-free summer year.
*   **Why Cards?** Again, cards excel at presenting key figures in an easily scannable and digestible format. They immediately convey the severity of the ice loss.
*   **Alternatives Discarded:**
    *   **Table:** Less visually impactful for highlighting key statistics.
    *   **Text Paragraph:** Would bury the key numbers in text, reducing their prominence.

## 6. Annual Minimum Timeline (Line + Dot Plot with Annotations)

*   **Purpose:** To clearly show the long-term trend of declining Arctic sea ice extent specifically during September (the annual minimum). This is the most critical month for assessing the health of the Arctic sea ice cover.
*   **Why Line + Dot Plot?**
    *   **Line:** Emphasizes the dramatic downward trend over the satellite record (1979-present).
    *   **Dots:** Show individual yearly minimums, with tooltips for exact values.
    *   **Linear Trend Line:** A calculated linear regression (dashed line) visually represents the average rate of decline per decade, reinforcing the trend shown by the yearly data.
    *   **Color Scale on Dots:** While a simple blue line is used for the main trend, the dots are colored by extent (blue=high, red=low), subtly reinforcing the shift towards lower values over time.
    *   **Annotations:** Key elements like the baseline average (1979-2000), the "ice-free" threshold (1 million km²), and the record minimum year (highlighted dot and text) are explicitly marked to add context and highlight critical information.
*   **Alternatives Discarded:**
    *   **Bar Chart:** Less effective for showing the continuous trend and could be cluttered.
    *   **Area Chart:** Could work but might obscure the baseline and threshold reference lines compared to a line plot.

## 7. Monthly Sea Ice Comparison (Multi-Line Plot)

*   **Purpose:** To illustrate how sea ice extent has changed throughout the entire year, comparing different decades. This shows that the decline isn't just happening at the minimum (September) but across all seasons.
*   **Why Multi-Line Plot?** Ideal for comparing the seasonal cycle (the rise and fall of ice extent through the months) across different time periods (1979-1989, 2000-2010, 2015-2023). The vertical gap between the lines for any given month represents the amount of ice lost between those periods.
    *   **Curve:** Using `curve: "cardinal"` smooths the lines slightly, emphasizing the cyclical pattern.
    *   **Color Coding:** Distinct, sequential colors (blue -> yellow -> red) represent the different time periods, clearly showing the progression towards lower ice extents in more recent decades.
    *   **Annotations:** Text labels highlight the typical annual maximum (March) and minimum (September) points on the earliest line for reference.
*   **Alternatives Discarded:**
    *   **Multiple Small Charts (Small Multiples):** Could show each period separately, but direct comparison on a single plot is more effective here.
    *   **Stacked Area Chart:** Not appropriate, as the goal is comparison between time periods, not showing parts of a whole.
    *   **Heatmap (Month vs. Year):** Could show the data but might be less intuitive for comparing specific decadal averages of the seasonal cycle.

## 8. Arctic Sea Ice Visualization (Map with Line Overlays)

*   **Purpose:** To provide a geographic representation of the sea ice retreat, showing the spatial difference between the average minimum ice extent in an early period (1979-1989) and a recent period (2015-2023).
*   **Why Map with Lines?**
    *   **Map:** Essential for visualizing geographic data.
    *   **Azimuthal Equidistant Projection:** A polar projection centered on the North Pole is the most appropriate way to view the Arctic region.
    *   **Line Overlays:** Instead of filling areas (which would require complex polygon data representing the ice edge), simplified circular lines *approximate* the average ice extent for the two periods. This effectively conveys the concept of the ice edge retreating towards the pole.
    *   **Color Coding:** Consistent colors (blue for early, red for late) link back to the monthly comparison chart and clearly distinguish the two periods.
    *   **Context:** Land masses, graticules, and key labels (North Pole, Canada, Russia, etc.) provide necessary geographic context.
*   **Alternatives Discarded:**
    *   **Actual Ice Extent Polygons:** While more accurate, plotting actual average ice extent polygons is significantly more complex, requiring specialized geospatial data and processing. The simplified line representation was chosen for feasibility within the dashboard context while still conveying the core message of retreat.
    *   **Raster Map:** Could show ice concentration, but comparing two distinct average *extents* is effectively done with boundary lines.
    *   **Side-by-Side Maps:** Showing two separate maps would make the direct comparison of the retreat less immediate than overlaying the lines on a single map.

## 9. Annual CO₂ Emissions by Country (Stacked Area Chart)

*   **Purpose:** To show the historical trend of annual CO₂ emissions from 1970 onwards, broken down by the top contributing countries and an 'Other' category. This visualization highlights both the overall growth in global emissions and the relative contributions of different nations over time.
*   **Why Stacked Area Chart?**
    *   **Shows Trend:** Effectively displays the change in total emissions over time (the upper edge of the chart).
    *   **Shows Composition:** The stacked layers clearly illustrate the contribution of each country (or 'Other') to the total in any given year. The area of each colored band represents that country's emissions.
    *   **Handles Many Categories:** Suitable for showing contributions from multiple categories (top countries + Other) simultaneously.
    *   **Interaction:** Allows highlighting a specific country via the budget chart's controls, dimming other areas to focus attention.
*   **Alternatives Discarded:**
    *   **Multi-Line Chart:** Could show individual country trends but wouldn't clearly represent the total global emissions or the part-to-whole relationship each year.
    *   **Stacked Bar Chart:** Similar to the stacked area chart but might imply discrete yearly totals rather than a continuous trend. Could also look very busy with many bars.
    *   **100% Stacked Area Chart:** Would show the *proportion* each country contributes but would lose the information about the *absolute* total emissions growth over time, which is a key message.

## 10. Cumulative Global CO₂ Emissions vs. Carbon Budget (Interactive Line Chart)

*   **Purpose:** To visualize the core concept of the carbon budget: comparing cumulative historical and ongoing global CO₂ emissions against the estimated remaining budget for specific climate targets (1.5°C or 2.0°C) with different probability levels.
*   **Why Interactive Line Chart?**
    *   **Cumulative Trend:** A line chart is the standard way to show cumulative values increasing over time. The steepness of the line indicates the rate of emission.
    *   **Budget Comparison:** A horizontal dashed line clearly represents the fixed carbon budget limit. The point where the cumulative emissions line intersects (or will intersect) this budget line is critical.
    *   **Interactivity:** Controls (radio buttons for temperature target, dropdown for probability, dropdown for country highlight) allow users to explore different scenarios and see their impact on the budget and the contribution of specific nations.
    *   **Annotations:** Text labels and points clearly mark the budget limit and the current cumulative emissions level, making the key comparison explicit.
    *   **Highlighting:** Optionally overlaying a specific country's cumulative emissions (as a dashed line) provides context on national contributions relative to the global total and budget.
*   **Alternatives Discarded:**
    *   **Area Chart:** While it could show the cumulative total, it might obscure the budget line. A simple line focuses attention on the trajectory towards the limit.
    *   **Static Chart:** Would only be able to show one budget scenario at a time. Interactivity is crucial for exploring the different targets and probabilities inherent in carbon budget science.
    *   **Bar Chart:** Not suitable for showing cumulative data over time.

## 11. Emissions by Sector for Top Emitters (Stacked Bar Chart)

*   **Purpose:** To show the breakdown of CO₂ emissions by major economic sectors (Energy, Industry, Transportation, Buildings, Other) for the top 15 emitting countries in the most recent year available. This highlights where emissions originate within the largest contributing nations.
*   **Why Stacked Bar Chart?**
    *   **Comparison Across Countries:** Placing bars side-by-side (or vertically aligned as done here with `Plot.barX`) allows easy comparison of *total* emissions across different countries (the total length of each bar).
    *   **Shows Composition:** Stacking segments within each bar clearly shows the *proportion* each sector contributes to that country's total emissions.
    *   **Categorical Data:** Well-suited for comparing a quantitative value (emissions) across two categorical variables (country and sector).
*   **Alternatives Discarded:**
    *   **Multiple Pie Charts:** Could show the sector breakdown for each country, but comparing proportions across multiple pies is notoriously difficult for humans.
    *   **Grouped Bar Chart:** Could show bars for each sector side-by-side for each country, but this would make it harder to compare the *total* emissions of each country and could become very cluttered.
    *   **Treemap:** Could show the breakdown (and was used in an earlier version, see `sectorTreemapData`), but a stacked bar chart often makes direct comparison of the primary categories (countries in this case) easier.

## Overall Narrative Flow

The visualizations are ordered to tell a story:
1.  Start with the big picture summary (Key Numbers).
2.  Show the overall global trend over time (Timeline).
3.  Introduce complexity by comparing hemispheres (Hemisphere Comparison).
4.  Provide geographic detail showing *where* the warming is happening most intensely (Maps).
5.  Conclude with key takeaways and data sources.

This progression moves from simple to complex, providing context and building understanding step-by-step.

## Overall Narrative Flow (Arctic Sea Ice)

Similar to the temperature dashboard, the story progresses logically:
1.  Start with the alarming summary statistics (Scorecard).
2.  Show the primary trend – the decline of the annual minimum (Timeline).
3.  Expand to show the decline affects all months (Monthly Comparison).
4.  Visualize the geographic impact of the retreat (Map).
5.  Conclude with key takeaways and data sources.

## Overall Narrative Flow (Carbon Budget)

The carbon budget dashboard focuses on the urgency of emissions reduction:
1.  Show the history of *annual* emissions and identify the major contributors (Stacked Area Chart).
2.  Introduce the *cumulative* emissions concept and compare it directly to the remaining budgets under different scenarios, allowing user interaction (Interactive Line Chart).
3.  Provide context on *where* emissions come from within the top emitting countries (Sector Breakdown Bar Chart).
4.  Conclude with key takeaways emphasizing the shrinking budget and the need for action.

This flow moves from historical context to the present challenge (the budget) and then provides actionable insight (sectoral sources).