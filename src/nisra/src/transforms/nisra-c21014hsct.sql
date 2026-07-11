-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census Year" AS BIGINT) AS census_year,
    "HSCT" AS hsct,
    "Health and Social Care Trust" AS health_and_social_care_trust,
    CAST("HEALTH_CONDITION_MENTAL_HEALTH" AS BIGINT) AS health_condition_mental_health,
    "Emotional, psychological or mental health" AS emotional_psychological_or_mental_health,
    CAST("AGE_BAND_AGG8" AS BIGINT) AS age_band_agg8,
    "Age (8 cats)" AS age_8_cats,
    CAST("UR_SEX" AS BIGINT) AS ur_sex,
    "Sex" AS sex,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-c21014hsct"
