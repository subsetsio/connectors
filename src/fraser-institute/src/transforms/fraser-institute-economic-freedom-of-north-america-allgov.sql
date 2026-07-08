SELECT
    CAST(year AS INTEGER)            AS year,
    country,
    state_province,
    iso_code,
    type                              AS jurisdiction_type,
    TRY_CAST(summary_index AS DOUBLE) AS economic_freedom_summary,
    TRY_CAST(rank AS INTEGER)         AS rank,
    TRY_CAST(quantile AS INTEGER)     AS quintile,
    TRY_CAST(area1 AS DOUBLE)         AS government_spending,
    TRY_CAST(area2 AS DOUBLE)         AS taxes,
    TRY_CAST(area3 AS DOUBLE)         AS labor_market_freedom,
    TRY_CAST(area4 AS DOUBLE)         AS legal_system_property_rights,
    TRY_CAST(area5 AS DOUBLE)         AS sound_money,
    TRY_CAST(area6 AS DOUBLE)         AS freedom_to_trade_internationally
FROM "fraser-institute-economic-freedom-of-north-america-allgov"
WHERE iso_code IS NOT NULL AND iso_code <> ''
