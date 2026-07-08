SELECT
    CAST(date AS DATE)                    AS date,
    region,
    ROUND(none, 2)                        AS none_pct,
    ROUND(GREATEST(d0 - d1, 0), 2)        AS d0_pct,
    ROUND(GREATEST(d1 - d2, 0), 2)        AS d1_pct,
    ROUND(GREATEST(d2 - d3, 0), 2)        AS d2_pct,
    ROUND(GREATEST(d3 - d4, 0), 2)        AS d3_pct,
    ROUND(d4, 2)                          AS d4_pct
FROM "us-drought-monitor-drought-severity"
WHERE date IS NOT NULL AND region IS NOT NULL
