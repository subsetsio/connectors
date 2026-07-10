-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("ID_CUBE" AS BIGINT) AS id_cube,
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    "CD_SEX" AS cd_sex,
    "CD_AGE" AS cd_age,
    "CD_CNTRY_BTH" AS cd_cntry_bth,
    "TX_CNTRY_BTH_DESCR_DE" AS tx_cntry_bth_descr_de,
    "TX_CNTRY_BTH_DESCR_EN" AS tx_cntry_bth_descr_en,
    "TX_CNTRY_BTH_DESCR_FR" AS tx_cntry_bth_descr_fr,
    "TX_CNTRY_BTH_DESCR_NL" AS tx_cntry_bth_descr_nl,
    "CD_NATLTY" AS cd_natlty,
    "TX_NATLTY_DESCR_DE" AS tx_natlty_descr_de,
    "TX_NATLTY_DESCR_EN" AS tx_natlty_descr_en,
    "TX_NATLTY_DESCR_FR" AS tx_natlty_descr_fr,
    "TX_NATLTY_DESCR_NL" AS tx_natlty_descr_nl,
    "CD_NUTS_LVL3" AS cd_nuts_lvl3,
    "TX_NUTS_LVL3_DESCR_DE" AS tx_nuts_lvl3_descr_de,
    "TX_NUTS_LVL3_DESCR_EN" AS tx_nuts_lvl3_descr_en,
    "TX_NUTS_LVL3_DESCR_FR" AS tx_nuts_lvl3_descr_fr,
    "TX_NUTS_LVL3_DESCR_NL" AS tx_nuts_lvl3_descr_nl,
    "CD_PROPERTY" AS cd_property,
    "TX_PROPERTY_DESCR_DE" AS tx_property_descr_de,
    "TX_PROPERTY_DESCR_EN" AS tx_property_descr_en,
    "TX_PROPERTY_DESCR_FR" AS tx_property_descr_fr,
    "TX_PROPERTY_DESCR_NL" AS tx_property_descr_nl,
    CAST("MS_VALUE" AS BIGINT) AS ms_value
FROM "statbel-nodeid5718"
