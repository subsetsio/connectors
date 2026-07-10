-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "TX_MUNTY_DESCR_FR" AS tx_munty_descr_fr,
    "TX_MUNTY_DESCR_NL" AS tx_munty_descr_nl,
    "TX_MUNTY_DESCR_DE" AS tx_munty_descr_de,
    "TX_MUNTY_DESCR_EN" AS tx_munty_descr_en,
    "cd_sector",
    CAST("total_huisH" AS BIGINT) AS total_huish,
    CAST("total_wagens" AS BIGINT) AS total_wagens
FROM "statbel-nodeid4847"
