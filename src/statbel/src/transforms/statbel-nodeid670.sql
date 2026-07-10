-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("NM_YR" AS BIGINT) AS nm_yr,
    CAST("NM_MTH" AS BIGINT) AS nm_mth,
    "CD_COICOP" AS cd_coicop,
    "TX_COICOP_FR_LVL1" AS tx_coicop_fr_lvl1,
    "TX_COICOP_NL_LVL1" AS tx_coicop_nl_lvl1,
    "TX_COICOP_EN_LVL1" AS tx_coicop_en_lvl1,
    "TX_COICOP_FR_LVL2" AS tx_coicop_fr_lvl2,
    "TX_COICOP_NL_LVL2" AS tx_coicop_nl_lvl2,
    "TX_COICOP_EN_LVL2" AS tx_coicop_en_lvl2,
    "TX_COICOP_FR_LVL3" AS tx_coicop_fr_lvl3,
    "TX_COICOP_NL_LVL3" AS tx_coicop_nl_lvl3,
    "TX_COICOP_EN_LVL3" AS tx_coicop_en_lvl3,
    "TX_COICOP_FR_LVL4" AS tx_coicop_fr_lvl4,
    "TX_COICOP_NL_LVL4" AS tx_coicop_nl_lvl4,
    "TX_COICOP_EN_LVL4" AS tx_coicop_en_lvl4,
    "TX_COICOP_FR_LVL5" AS tx_coicop_fr_lvl5,
    "TX_COICOP_NL_LVL5" AS tx_coicop_nl_lvl5,
    "TX_COICOP_EN_LVL5" AS tx_coicop_en_lvl5,
    "MS_CPI_IDX" AS ms_cpi_idx,
    "MS_CPI_WT" AS ms_cpi_wt,
    CAST("NM_CD_COICOP_LVL" AS BIGINT) AS nm_cd_coicop_lvl,
    "MS_CPI_INFL" AS ms_cpi_infl,
    CAST("NM_BASE_YR" AS BIGINT) AS nm_base_yr
FROM "statbel-nodeid670"
