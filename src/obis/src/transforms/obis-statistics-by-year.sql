SELECT
    CAST(year AS INTEGER) AS year,
    CAST(records AS BIGINT) AS records
FROM "obis-statistics-by-year"
WHERE year IS NOT NULL
ORDER BY year
