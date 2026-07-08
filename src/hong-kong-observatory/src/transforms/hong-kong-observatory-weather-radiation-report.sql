SELECT
    strptime(report_date, '%Y%m%d')::DATE AS date,
    station,
    metric,
    CAST(TRY_CAST(value AS DOUBLE) AS DOUBLE) AS value
FROM "hong-kong-observatory-weather-radiation-report"
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
