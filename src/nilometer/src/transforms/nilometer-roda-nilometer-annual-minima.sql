SELECT
    CAST(year AS INTEGER)      AS year,
    CAST(min_level AS INTEGER) AS min_level
FROM "nilometer-roda-nilometer-annual-minima"
WHERE year IS NOT NULL AND min_level IS NOT NULL
ORDER BY year
