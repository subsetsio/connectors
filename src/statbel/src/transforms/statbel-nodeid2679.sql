-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    CAST("MM" AS BIGINT) AS mm,
    CAST("YYYY" AS BIGINT) AS yyyy,
    "CD_AGE" AS cd_age,
    "MS_SEX" AS ms_sex,
    "CD_PLC_DTH" AS cd_plc_dth,
    CAST("TOTAL" AS BIGINT) AS total,
    "BREAK" AS break
FROM "statbel-nodeid2679"
