---
toc: false
sidebar: false
pager: false
---

<div class="hero">
  <h1>Climate in Crisis</h1>
  <h2>Visualizing Our Changing Planet</h2>
  <a href="/global-temperature-dashboard">Explore Temperature Data<span style="display: inline-block; margin-left: 0.25rem;">→</span></a>
</div>

<div class="grid grid-cols-1" style="grid-auto-rows: 300px;">
  <div class="card">
    <h2>Project Overview</h2>
    <p>Welcome to "Climate in Crisis: Visualizing Our Changing Planet," a data visualization portfolio focused on climate change evidence, impacts, and potential solutions. Explore interactive visualizations of global temperature anomalies, Arctic sea ice decline, and more.</p>
  </div>
</div>

---

## Available Visualizations

<div class="grid grid-cols-2">
  <div class="card">
    <h3>Global Temperature Anomalies</h3>
    <p>Explore historical temperature data showing global warming trends from 1880 to present day. Compare the Northern and Southern hemispheres and analyze temperature distribution by decade.</p>
    <a href="/global-temperature-dashboard">Explore →</a>
  </div>
  <div class="card">
    <h3>Arctic Sea Ice</h3>
    <p>Visualization of dramatic Arctic sea ice decline over time, with seasonal patterns and long-term trends showing the impacts of global warming on polar regions.</p>
    <a href="/arctic-sea-ice-dashboard">Explore →</a>
  </div>
  <div class="card">
    <h3>Extreme Weather Events</h3>
    <p>Coming soon: Explore the increasing frequency and intensity of extreme weather events related to climate change.</p>
  </div>
  <div class="card">
    <h3>Carbon Emissions</h3>
    <p>Coming soon: Visualize global carbon emissions by country, sector, and historical trends.</p>
  </div>
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

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>
