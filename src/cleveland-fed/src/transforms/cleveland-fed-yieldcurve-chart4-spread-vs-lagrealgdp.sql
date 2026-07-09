SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "spread",
    "real_gdp",
    "recession" = 100 AS nber_recession
FROM "cleveland-fed-yieldcurve-chart4-spread-vs-lagrealgdp"
