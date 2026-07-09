SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "spread",
    "real_gdp_growth",
    "real_gdp_growth_forecast"
FROM "cleveland-fed-yieldcurve-chart1-spread-vs-gdpgrowth-w-forecast"
