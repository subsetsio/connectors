SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "recession_probability",
    "recession_probability_forecast",
    "recession" = 1000 AS nber_recession
FROM "cleveland-fed-yieldcurve-chart2-recession-probability-w-forecast"
