-- WPP2024 fertility by 5-year age group of mother (Medium variant).
-- Published only for the Medium (standard) projection variant.
SELECT
    CAST(LocID AS BIGINT) AS location_id,
    Location AS location_name,
    CAST(Time AS BIGINT) AS year,
    AgeGrp AS age_group,
    CAST(AgeGrpStart AS BIGINT) AS age_start,
    CAST(ASFR AS DOUBLE) AS fertility_rate,
    CAST(PASFR AS DOUBLE) AS fertility_rate_pct,
    CAST(Births AS DOUBLE) AS births
FROM "un-population-division-fertility-by-age5"
WHERE LocID IS NOT NULL AND Variant = 'Medium'
