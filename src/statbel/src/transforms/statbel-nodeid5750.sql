-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "CD_LAU" AS cd_lau,
    "CD_MUNTY_REFNIS" AS cd_munty_refnis,
    "TX_DESCR_DE" AS tx_descr_de,
    "TX_DESCR_EN" AS tx_descr_en,
    "TX_DESCR_FR" AS tx_descr_fr,
    "TX_DESCR_NL" AS tx_descr_nl,
    "DT_VLDT_STRT" AS dt_vldt_strt,
    strptime("DT_VLDT_STOP", '%d/%m/%Y')::DATE AS dt_vldt_stop,
    "CD_LVL_SUP" AS cd_lvl_sup,
    CAST("CD_LVL" AS BIGINT) AS cd_lvl
FROM "statbel-nodeid5750"
