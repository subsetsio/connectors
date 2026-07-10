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
    "CD_POTENTIAL_LF_AGE" AS cd_potential_lf_age,
    "CD_PROPERTY" AS cd_property,
    "TX_PROPERTY_DESCR_DE" AS tx_property_descr_de,
    "TX_PROPERTY_DESCR_EN" AS tx_property_descr_en,
    "TX_PROPERTY_DESCR_FR" AS tx_property_descr_fr,
    "TX_PROPERTY_DESCR_NL" AS tx_property_descr_nl,
    CAST("MS_VALUE" AS DOUBLE) AS ms_value
FROM "statbel-nodeid5724"
