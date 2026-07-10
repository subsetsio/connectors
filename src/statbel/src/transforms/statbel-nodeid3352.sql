-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    CAST("MONTH" AS BIGINT) AS month,
    CAST("YEAR" AS BIGINT) AS year,
    "CD_AGE" AS cd_age,
    "MS_SEX" AS ms_sex,
    "CD_PLC_DTH" AS cd_plc_dth,
    CAST("COUNT" AS BIGINT) AS count
FROM "statbel-nodeid3352"
