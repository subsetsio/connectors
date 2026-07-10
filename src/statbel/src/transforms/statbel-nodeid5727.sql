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
    "CD_PVRTY_AGE" AS cd_pvrty_age,
    "CD_ISCED_2011" AS cd_isced_2011,
    "TX_ISCED_2011_DESCR_DE" AS tx_isced_2011_descr_de,
    "TX_ISCED_2011_DESCR_EN" AS tx_isced_2011_descr_en,
    "TX_ISCED_2011_DESCR_FR" AS tx_isced_2011_descr_fr,
    "TX_ISCED_2011_DESCR_NL" AS tx_isced_2011_descr_nl,
    "CD_PVRTY_NTLY" AS cd_pvrty_ntly,
    "TX_PVRTY_NTLY_DESCR_DE" AS tx_pvrty_ntly_descr_de,
    "TX_PVRTY_NTLY_DESCR_EN" AS tx_pvrty_ntly_descr_en,
    "TX_PVRTY_NTLY_DESCR_FR" AS tx_pvrty_ntly_descr_fr,
    "TX_PVRTY_NTLY_DESCR_NL" AS tx_pvrty_ntly_descr_nl,
    "CD_PVRTY_BTH_CNTRY" AS cd_pvrty_bth_cntry,
    "TX_PVRTY_BTH_CNTRY_DESCR_DE" AS tx_pvrty_bth_cntry_descr_de,
    "TX_PVRTY_BTH_CNTRY_DESCR_EN" AS tx_pvrty_bth_cntry_descr_en,
    "TX_PVRTY_BTH_CNTRY_DESCR_FR" AS tx_pvrty_bth_cntry_descr_fr,
    "TX_PVRTY_BTH_CNTRY_DESCR_NL" AS tx_pvrty_bth_cntry_descr_nl,
    "CD_PVRTY_OCPTN_STS" AS cd_pvrty_ocptn_sts,
    "TX_PVRTY_OCPTN_STS_DESCR_DE" AS tx_pvrty_ocptn_sts_descr_de,
    "TX_PVRTY_OCPTN_STS_DESCR_EN" AS tx_pvrty_ocptn_sts_descr_en,
    "TX_PVRTY_OCPTN_STS_DESCR_FR" AS tx_pvrty_ocptn_sts_descr_fr,
    "TX_PVRTY_OCPTN_STS_DESCR_NL" AS tx_pvrty_ocptn_sts_descr_nl,
    "CD_PVRTY_INCM_QNTL" AS cd_pvrty_incm_qntl,
    "CD_NUTS_LVL2" AS cd_nuts_lvl2,
    "TX_NUTS_LVL2_DESCR_DE" AS tx_nuts_lvl2_descr_de,
    "TX_NUTS_LVL2_DESCR_EN" AS tx_nuts_lvl2_descr_en,
    "TX_NUTS_LVL2_DESCR_FR" AS tx_nuts_lvl2_descr_fr,
    "TX_NUTS_LVL2_DESCR_NL" AS tx_nuts_lvl2_descr_nl,
    "CD_PROPERTY" AS cd_property,
    "TX_PROPERTY_DESCR_DE" AS tx_property_descr_de,
    "TX_PROPERTY_DESCR_EN" AS tx_property_descr_en,
    "TX_PROPERTY_DESCR_FR" AS tx_property_descr_fr,
    "TX_PROPERTY_DESCR_NL" AS tx_property_descr_nl,
    CAST("MS_VALUE" AS DOUBLE) AS ms_value
FROM "statbel-nodeid5727"
