SELECT
    CAST(year AS INTEGER) AS year,
    TRY_CAST(ec AS DOUBLE) AS ec
FROM "port-of-la-b3i5-86hy"
WHERE year IS NOT NULL
