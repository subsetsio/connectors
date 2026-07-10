-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "TX_MUNTY_DESCR_FR" AS tx_munty_descr_fr,
    "TX_MUNTY_DESCR_NL" AS tx_munty_descr_nl,
    "TX_MUNTY_DESCR_DE" AS tx_munty_descr_de,
    "TX_MUNTY_DESCR_EN" AS tx_munty_descr_en,
    "cd_sector",
    "tx_sec_descr_fr",
    "tx_sec_descr_nl",
    "tx_sec_descr_de",
    CAST("ms_tot_hh" AS BIGINT) AS ms_tot_hh,
    CAST("ms_tot_cars" AS BIGINT) AS ms_tot_cars
FROM "statbel-nodeid6441"
