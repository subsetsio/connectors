-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census Year" AS BIGINT) AS census_year,
    "NI" AS ni,
    "Northern Ireland" AS northern_ireland,
    CAST("HEALTH_CONDITION_MOBILITY_PHYSICAL" AS BIGINT) AS health_condition_mobility_physical,
    "Mobility or dexterity difficulty that limits basic physical activities" AS mobility_or_dexterity_difficulty_that_limits_basic_physical_activities,
    CAST("AGE_BAND_AGG8" AS BIGINT) AS age_band_agg8,
    "Age (8 cats)" AS age_8_cats,
    CAST("UR_SEX" AS BIGINT) AS ur_sex,
    "Sex" AS sex,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-c21019ni"
