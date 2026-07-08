SELECT location, metric, period, CAST(value AS DOUBLE) AS value
FROM "knmi-climate-normals-1991-2020-precipitation-normals-by-district-1"
WHERE value IS NOT NULL
