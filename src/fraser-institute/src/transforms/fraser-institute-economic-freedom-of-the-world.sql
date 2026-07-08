SELECT
    CAST(year AS INTEGER)            AS year,
    country,
    iso_code,
    TRY_CAST(summary_index AS DOUBLE) AS economic_freedom_summary,
    TRY_CAST(rank AS INTEGER)         AS world_rank,
    TRY_CAST(quartile AS INTEGER)     AS quartile,
    TRY_CAST(area1 AS DOUBLE)         AS size_of_government,
    TRY_CAST(area1rank AS INTEGER)    AS size_of_government_rank,
    TRY_CAST(area2 AS DOUBLE)         AS legal_system_property_rights,
    TRY_CAST(area2rank AS INTEGER)    AS legal_system_property_rights_rank,
    TRY_CAST(area3 AS DOUBLE)         AS sound_money,
    TRY_CAST(area3rank AS INTEGER)    AS sound_money_rank,
    TRY_CAST(area4 AS DOUBLE)         AS freedom_to_trade_internationally,
    TRY_CAST(area4rank AS INTEGER)    AS freedom_to_trade_internationally_rank,
    TRY_CAST(area5 AS DOUBLE)         AS regulation,
    TRY_CAST(area5rank AS INTEGER)    AS regulation_rank
FROM "fraser-institute-economic-freedom-of-the-world"
WHERE iso_code IS NOT NULL AND iso_code <> ''
