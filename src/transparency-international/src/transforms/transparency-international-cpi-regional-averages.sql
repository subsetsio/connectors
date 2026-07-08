SELECT
    region,
    CAST(year AS INTEGER)          AS year,
    CAST(avg_cpi_score AS DOUBLE)  AS avg_cpi_score,
    CAST(n AS INTEGER)             AS n
FROM "transparency-international-cpi-regional-averages"
WHERE avg_cpi_score IS NOT NULL
