-- Zillow Home Value Forecast (ZHVF) by geography, vintage, and forecast horizon.
-- Pivots the long raw (one row per region/base_date/forecast_date/metric) to a
-- wide table with raw and smoothed/seasonally-adjusted growth forecasts.
SELECT
    CAST(base_date AS DATE) AS base_date,
    CAST(date AS DATE) AS forecast_date,
    CAST(region_id AS BIGINT) AS region_id,
    ANY_VALUE(region_type) AS region_type,
    ANY_VALUE(region_name) AS region_name,
    ANY_VALUE(state_code) AS state_code,
    MAX(value) FILTER (WHERE metric = 'forecast_smoothed_seasonally_adjusted') AS forecast_smoothed_seasonally_adjusted,
    MAX(value) FILTER (WHERE metric = 'forecast_raw') AS forecast_raw
FROM "zillow-forecast"
GROUP BY region_id, base_date, date
