-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("LVL_ISCED_F2013" AS BIGINT) AS lvl_isced_f2013,
    "CD_ISCED_F2013" AS cd_isced_f2013,
    "CD_SUP_ISCED_F2013" AS cd_sup_isced_f2013,
    "TX_ISCED_F2013_EN" AS tx_isced_f2013_en,
    "TX_ISCED_F2013_FR" AS tx_isced_f2013_fr,
    "TX_ISCED_F2013_NL" AS tx_isced_f2013_nl,
    "DT_VLDT_START" AS dt_vldt_start,
    strptime("DT_VLDT_END", '%d/%m/%Y')::DATE AS dt_vldt_end
FROM "statbel-nodeid736"
