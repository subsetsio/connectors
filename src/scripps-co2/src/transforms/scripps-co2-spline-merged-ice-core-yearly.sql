SELECT CAST(year_ce AS DOUBLE) AS year_ce,
       CAST(co2 AS DOUBLE)     AS co2
FROM "scripps-co2-spline-merged-ice-core-yearly"
WHERE co2 IS NOT NULL
