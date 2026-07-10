-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("ID_CUBE" AS BIGINT) AS id_cube,
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    "CD_QUARTER" AS cd_quarter,
    "CD_SEX" AS cd_sex,
    "CD_EMPMT_AGE" AS cd_empmt_age,
    "CD_NUTS_LVL2" AS cd_nuts_lvl2,
    "TX_NUTS_LVL2_DESCR_DE" AS tx_nuts_lvl2_descr_de,
    "TX_NUTS_LVL2_DESCR_EN" AS tx_nuts_lvl2_descr_en,
    "TX_NUTS_LVL2_DESCR_FR" AS tx_nuts_lvl2_descr_fr,
    "TX_NUTS_LVL2_DESCR_NL" AS tx_nuts_lvl2_descr_nl,
    "CD_ISCED_2011" AS cd_isced_2011,
    "TX_ISCED_2011_DESCR_DE" AS tx_isced_2011_descr_de,
    "TX_ISCED_2011_DESCR_EN" AS tx_isced_2011_descr_en,
    "TX_ISCED_2011_DESCR_FR" AS tx_isced_2011_descr_fr,
    "TX_ISCED_2011_DESCR_NL" AS tx_isced_2011_descr_nl,
    "CD_PROPERTY" AS cd_property,
    "TX_PROPERTY_DESCR_DE" AS tx_property_descr_de,
    "TX_PROPERTY_DESCR_EN" AS tx_property_descr_en,
    "TX_PROPERTY_DESCR_FR" AS tx_property_descr_fr,
    "TX_PROPERTY_DESCR_NL" AS tx_property_descr_nl,
    "MS_VALUE" AS ms_value
FROM "statbel-nodeid5759"
