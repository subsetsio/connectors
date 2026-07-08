SELECT
    CAST(year AS INTEGER)            AS year,
    country,
    state_province,
    iso_code,
    TRY_CAST(summary_index AS DOUBLE) AS economic_freedom_summary,
    TRY_CAST(rank AS INTEGER)         AS rank,
    TRY_CAST(quantile AS INTEGER)     AS quintile,
    TRY_CAST(area1 AS DOUBLE)         AS government_spending,
    TRY_CAST(area2 AS DOUBLE)         AS taxes,
    TRY_CAST(area3 AS DOUBLE)         AS labor_market_freedom
FROM "fraser-institute-economic-freedom-of-north-america-subnational"
WHERE iso_code IS NOT NULL AND iso_code <> ''
