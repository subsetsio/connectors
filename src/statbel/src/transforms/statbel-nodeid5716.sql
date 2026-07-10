-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("ID_CUBE" AS BIGINT) AS id_cube,
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    "CD_AGE" AS cd_age,
    "CD_REFNIS" AS cd_refnis,
    "CD_NUTS" AS cd_nuts,
    "TX_NUTS_DESCR_FR" AS tx_nuts_descr_fr,
    "TX_NUTS_DESCR_NL" AS tx_nuts_descr_nl,
    "TX_NUTS_DESCR_EN" AS tx_nuts_descr_en,
    "TX_NUTS_DESCR_DE" AS tx_nuts_descr_de,
    "CD_PROPERTY" AS cd_property,
    "TX_PROPERTY_DESCR_FR" AS tx_property_descr_fr,
    "TX_PROPERTY_DESCR_NL" AS tx_property_descr_nl,
    "TX_PROPERTY_DESCR_EN" AS tx_property_descr_en,
    "TX_PROPERTY_DESCR_DE" AS tx_property_descr_de,
    CAST("CD_NUTS_LEVEL" AS BIGINT) AS cd_nuts_level,
    CAST("MS_VALUE" AS DOUBLE) AS ms_value
FROM "statbel-nodeid5716"
