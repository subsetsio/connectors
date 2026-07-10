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
    "TX_HH_TYPE_FR" AS tx_hh_type_fr,
    "TX_HH_TYPE_NL" AS tx_hh_type_nl,
    "TX_HH_TYPE_DE" AS tx_hh_type_de,
    "TX_HH_TYPE_EN" AS tx_hh_type_en,
    "CD_CARS_PER_HH" AS cd_cars_per_hh,
    CAST("MS_NUM_HH" AS BIGINT) AS ms_num_hh,
    CAST("MS_NUM_CARS" AS BIGINT) AS ms_num_cars
FROM "statbel-nodeid2777"
