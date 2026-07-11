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
    CAST("MAR_CP_STATUS_AGG5" AS BIGINT) AS mar_cp_status_agg5,
    "Marital and civil partnership status" AS marital_and_civil_partnership_status,
    CAST("AGE_BAND_5YR_16CAT" AS BIGINT) AS age_band_5yr_16cat,
    "Age (16 cats)" AS age_16_cats,
    CAST("UR_SEX" AS BIGINT) AS ur_sex,
    "Sex" AS sex,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-uk02"
