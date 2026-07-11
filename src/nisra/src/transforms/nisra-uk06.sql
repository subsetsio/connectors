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
    CAST("ETHNIC_GROUP_AGG5" AS BIGINT) AS ethnic_group_agg5,
    "Ethnic group" AS ethnic_group,
    CAST("AGE_BAND_5YR_85" AS BIGINT) AS age_band_5yr_85,
    "Age (20 cats)" AS age_20_cats,
    "UR_SEX" AS ur_sex,
    "Sex" AS sex,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-uk06"
