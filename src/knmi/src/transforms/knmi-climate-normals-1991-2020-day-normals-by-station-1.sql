SELECT location, metric, period, CAST(value AS DOUBLE) AS value
FROM "knmi-climate-normals-1991-2020-day-normals-by-station-1"
WHERE value IS NOT NULL
