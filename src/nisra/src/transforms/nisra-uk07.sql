-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census year" AS BIGINT) AS census_year,
    "CTRY24CD" AS ctry24cd,
    "Country" AS country,
    CAST("RELIGION_BELONG_TO_AGG7" AS BIGINT) AS religion_belong_to_agg7,
    "Religion" AS religion,
    CAST("AGE_BAND_5YR_85" AS BIGINT) AS age_band_5yr_85,
    "Age (20 cats)" AS age_20_cats,
    CAST("UR_SEX" AS BIGINT) AS ur_sex,
    "Sex" AS sex,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-uk07"
