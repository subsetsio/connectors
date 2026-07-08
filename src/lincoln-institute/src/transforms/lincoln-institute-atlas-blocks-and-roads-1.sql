SELECT city, country, region, latitude, longitude, metric, period,
       CAST(value AS DOUBLE) AS value
FROM "lincoln-institute-atlas-blocks-and-roads-1"
WHERE value IS NOT NULL
