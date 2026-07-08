SELECT
    CAST(date AS DATE)  AS date,
    pmms30              AS rate_30yr_fixed,
    pmms30p             AS points_30yr_fixed,
    pmms15              AS rate_15yr_fixed,
    pmms15p             AS points_15yr_fixed,
    pmms51              AS rate_5yr_arm,
    pmms51p             AS points_5yr_arm,
    pmms51m             AS margin_5yr_arm,
    pmms51spread        AS spread_5yr_arm
FROM "freddie-mac-mortgage-rates"
WHERE date IS NOT NULL
  AND pmms30 IS NOT NULL
