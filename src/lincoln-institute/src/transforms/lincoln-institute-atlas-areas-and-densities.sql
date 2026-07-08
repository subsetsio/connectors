SELECT city, country, region, latitude, longitude, metric, period,
       CAST(value AS DOUBLE) AS value
FROM "lincoln-institute-atlas-areas-and-densities"
WHERE value IS NOT NULL
