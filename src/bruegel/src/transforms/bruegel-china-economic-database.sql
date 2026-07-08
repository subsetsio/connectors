SELECT page, chart, series, x AS observation,
       TRY_CAST(value AS DOUBLE) AS value
FROM "bruegel-china-economic-database" WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
