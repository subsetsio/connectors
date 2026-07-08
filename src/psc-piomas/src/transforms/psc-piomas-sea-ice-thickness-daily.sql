SELECT
    CAST(date AS DATE)       AS date,
    CAST(thickness_m AS DOUBLE) AS thickness_m
FROM "psc-piomas-sea-ice-thickness-daily"
WHERE thickness_m IS NOT NULL
ORDER BY date
