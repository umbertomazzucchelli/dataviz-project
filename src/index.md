---
toc: false
sidebar: false
pager: true
---

<div class="hero">
  <h1>Climate Horizons</h1>
  <h2>Visualizing Earth's Transformation</h2>
  <a href="/global-temperature-dashboard">Begin Your Journey<span style="display: inline-block; margin-left: 0.25rem;">→</span></a>
</div>

<div class="content-wrapper">

# Our Planet's Story in Data

Welcome to **Climate Horizons** – where numbers tell Earth's most important story. This project lets you explore how our climate is changing through beautiful, easy-to-understand visualizations.

Instead of overwhelming you with complex charts and scientific jargon, we've created a journey that connects the dots: from rising temperatures to melting ice to extreme weather. Think of it as a guided tour of our changing planet, showing not just what's happening, but how these changes connect to each other – and to us.

## Your Climate Journey

Explore these interconnected dashboards to understand our changing world:

* **[Earth's Warming Story](/global-temperature-dashboard)** - Watch as our planet heats up over time, with some regions warming faster than others. See how temperatures have risen sharply since the 1970s and explore where warming is happening most rapidly.

* **[The Vanishing Ice Cap](/arctic-sea-ice-dashboard)** - Witness the dramatic shrinking of Arctic sea ice – Earth's natural air conditioner. Track how nearly half of the summer ice has disappeared in just a few decades and what this means for our future.

* **[When Weather Turns Wild](/extreme-weather-dashboard)** - Explore how storms, floods, heat waves and droughts are becoming more frequent and intense as our climate changes, with real impacts on communities worldwide.

* **[Our Carbon Budget](/carbon-budget-dashboard)** - Discover how much CO₂ we can still emit while limiting warming to 1.5°C or 2°C, and see how quickly we're spending this budget based on emissions from major countries.

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


<footer style="margin-top: 3rem; text-align: center; padding: 1rem 0;">
  <a href="https://github.com/umbertomazzucchelli/dataviz-project" target="_blank" style="display: inline-flex; align-items: center; color: var(--theme-foreground-muted); text-decoration: none; font-size: 0.9rem;">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 0.5rem;">
      <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
    </svg>
    View source on GitHub
  </a>
</footer>
