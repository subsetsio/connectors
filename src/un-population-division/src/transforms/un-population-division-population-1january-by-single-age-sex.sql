-- WPP2024 population on 1 January by single age and sex (Medium variant).
-- Published only for the Medium (standard) projection variant.
SELECT
    CAST(LocID AS BIGINT) AS location_id,
    Location AS location_name,
    NULLIF(TRIM(ISO3_code), '') AS iso3,
    NULLIF(TRIM(LocTypeName), '') AS location_type,
    CAST(Time AS BIGINT) AS year,
    AgeGrp AS age_group,
    CAST(AgeGrpStart AS BIGINT) AS age_start,
    CAST(PopTotal AS DOUBLE) AS population_total,
    CAST(PopMale AS DOUBLE) AS population_male,
    CAST(PopFemale AS DOUBLE) AS population_female
FROM "un-population-division-population-1january-by-single-age-sex"
WHERE LocID IS NOT NULL AND Variant = 'Medium'
