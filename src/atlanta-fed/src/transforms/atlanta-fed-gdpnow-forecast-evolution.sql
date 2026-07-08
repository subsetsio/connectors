SELECT DISTINCT
    CAST(forecast_date AS DATE)        AS forecast_date,
    CAST(quarter_end_date AS DATE)     AS quarter_end_date,
    CAST(gdp_nowcast AS DOUBLE)        AS gdp_nowcast,
    CAST(bea_advance_estimate AS DOUBLE) AS bea_advance_estimate,
    CAST(forecast_error AS DOUBLE)     AS forecast_error,
    data_release
FROM "atlanta-fed-gdpnow-forecast-evolution"
WHERE forecast_date IS NOT NULL
  AND gdp_nowcast IS NOT NULL
