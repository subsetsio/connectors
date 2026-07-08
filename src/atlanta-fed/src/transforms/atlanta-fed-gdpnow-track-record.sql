SELECT
    CAST(quarter_end_date AS DATE)     AS quarter_end_date,
    CAST(gdpnow_forecast AS DOUBLE)    AS gdpnow_forecast,
    CAST(bea_advance_estimate AS DOUBLE) AS bea_advance_estimate,
    CAST(release_date AS DATE)         AS release_date,
    CAST(error AS DOUBLE)              AS forecast_error,
    CAST(absolute_error AS DOUBLE)     AS absolute_error,
    CAST(squared_error AS DOUBLE)      AS squared_error
FROM "atlanta-fed-gdpnow-track-record"
WHERE quarter_end_date IS NOT NULL
  AND gdpnow_forecast IS NOT NULL
  AND bea_advance_estimate IS NOT NULL
