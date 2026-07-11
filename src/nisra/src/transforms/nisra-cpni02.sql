-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census year" AS BIGINT) AS census_year,
    "NIROI" AS niroi,
    "Ireland and Northern Ireland" AS ireland_and_northern_ireland,
    "AGE_BAND_AGG19" AS age_band_agg19,
    "Age (19 cats)" AS age_19_cats,
    "UR_SEX" AS ur_sex,
    "Sex" AS sex,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-cpni02"
