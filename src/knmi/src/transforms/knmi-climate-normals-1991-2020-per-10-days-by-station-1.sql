SELECT location, metric, period, CAST(value AS DOUBLE) AS value
FROM "knmi-climate-normals-1991-2020-per-10-days-by-station-1"
WHERE value IS NOT NULL
