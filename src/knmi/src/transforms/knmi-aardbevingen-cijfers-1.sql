SELECT CAST(year AS INTEGER) AS year,
       CAST(magnitude AS DOUBLE) AS magnitude,
       CAST(earthquake_count AS BIGINT) AS earthquake_count
FROM "knmi-aardbevingen-cijfers-1"
WHERE year IS NOT NULL AND earthquake_count IS NOT NULL
