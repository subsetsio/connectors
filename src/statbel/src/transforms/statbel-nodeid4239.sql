-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    "TX_RGN_DESCR_NL" AS tx_rgn_descr_nl,
    "TX_RGN_DESCR_FR" AS tx_rgn_descr_fr,
    "CD_SEX" AS cd_sex,
    "CD_AGE" AS cd_age,
    "CD_NATLTY" AS cd_natlty,
    "TX_NATLTY_NL" AS tx_natlty_nl,
    "TX_NATLTY_FR" AS tx_natlty_fr,
    CAST("FL_COHAB" AS BIGINT) AS fl_cohab,
    "TX_COHAB_NL" AS tx_cohab_nl,
    "TX_COHAB_FR" AS tx_cohab_fr,
    CAST("MS_COUNT" AS BIGINT) AS ms_count
FROM "statbel-nodeid4239"
