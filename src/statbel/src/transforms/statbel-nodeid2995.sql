-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CD_LAU" AS cd_lau,
    "CD_MUNTY_REFNIS" AS cd_munty_refnis,
    "TX_DESCR_DE" AS tx_descr_de,
    "TX_DESCR_EN" AS tx_descr_en,
    "TX_DESCR_FR" AS tx_descr_fr,
    "TX_DESCR_NL" AS tx_descr_nl,
    "DT_VLDT_STRT" AS dt_vldt_strt,
    "DT_VLDT_STOP" AS dt_vldt_stop,
    "CD_LVL_SUP" AS cd_lvl_sup,
    CAST("CD_LVL" AS BIGINT) AS cd_lvl
FROM "statbel-nodeid2995"
