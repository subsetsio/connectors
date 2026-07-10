-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "BE" AS be,
    "CD_REG" AS cd_reg,
    "CD_PROV" AS cd_prov,
    CAST("CD_SEX" AS BIGINT) AS cd_sex,
    "CD_AGE_CL" AS cd_age_cl,
    "CD_NATLTY" AS cd_natlty,
    "CD_DSCNT_CL" AS cd_dscnt_cl,
    "CD_ISCED_CL" AS cd_isced_cl,
    CAST("MS_POPULATION" AS BIGINT) AS ms_population
FROM "statbel-nodeid3454"
