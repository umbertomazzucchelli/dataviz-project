---
toc: false
sidebar: false
pager: true
---

<div class="hero">
  <h1>Climate Horizons</h1>
  <h2>Visualizing Earth's Transformation</h2>
  <a href="/global-temperature-dashboard">Explore Temperature Data<span style="display: inline-block; margin-left: 0.25rem;">→</span></a>
</div>

<div class="content-wrapper">

## Project Introduction

Welcome to "Climate in Crisis: Visualizing Our Changing Planet," a data visualization project that tells the interconnected story of climate change through three critical lenses. This project aims to create a streamlined narrative that begins with the fundamental driver - global warming - then shows its direct effects through Arctic sea ice decline, and finally demonstrates the consequences we're experiencing through extreme weather events.

By structuring the dashboards in this sequence, I aim to help users understand not just what's happening, but how these climate phenomena are connected, and ultimately, how human activities influence these patterns. My hope is that through effective data visualization, we can bridge the gap between complex climate science and public understanding, equipping users to recognize how their own actions can support climate solutions.

## Current Dashboards

The project currently consists of three interconnected dashboards in various stages of development:

* **Global Temperature Dashboard** - Visualizes temperature anomalies from 1880 to the present, including timeline visualizations showing the warming trend, hemisphere comparisons, and geographic heat maps displaying warming rates across different regions.

* **Arctic Sea Ice Dashboard** - Tracks the decline in sea ice extent since 1979, featuring timeline charts of annual minimum ice extent, monthly comparisons across decades, and a geographic visualization comparing historical ice coverage to recent years.

* **Extreme Weather Dashboard** - Examines severe weather event data, revealing increasing frequency and intensity of storms, floods, and heat waves. Includes interactive maps showing event locations and comparative analyses between past and present periods.

## Feedback Questions

1.How effective is the current narrative progression from global temperature to ice melt to extreme weather? Does it create a logical flow that helps understand climate change as a system?

2.The extreme weather dashboard includes both raw and normalized metrics to account for improved reporting over time. Is this dual approach helpful, or does it make the presentation too complex?

3.What additional components would be most valuable to add in the "human causes and solutions" section I'm planning to develop?

4.Does the current visualization approach effectively bridge the gap between scientific data and public understanding? What changes might make it more accessible?

</div>

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 4rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 1rem 0;
  padding: 1rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, #ff5e00, #d81356);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0 0 2rem 0;
  max-width: 34em;
  font-size: 24px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

.hero a {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(30deg, #ff5e00, #d81356);
  color: white;
  font-weight: 600;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.hero a:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.content-wrapper {
  width: 100%;
  max-width: 100%;
  padding: 0 2rem;
}

.content-wrapper h2 {
  width: 100%;
  max-width: 100%;
  margin-top: 2.5rem;
  margin-bottom: 1.5rem;
  font-size: 2rem;
}

.content-wrapper h3 {
  width: 100%;
  max-width: 100%;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.content-wrapper p,
.content-wrapper ul {
  width: 100%;
  max-width: 100%;
  margin-bottom: 1.5rem;
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
  
  .content-wrapper {
    padding: 0 4rem;
  }
}

@media (min-width: 1024px) {
  .content-wrapper {
    padding: 0 6rem;
  }
}

</style>
