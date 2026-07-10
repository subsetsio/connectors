-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "NM_YR" AS nm_yr,
    "NM_MTH" AS nm_mth,
    "CD_COICOP" AS cd_coicop,
    "TX_BASE_YR_DE_LVL1" AS tx_base_yr_de_lvl1,
    "TX_BASE_YR_EN_LVL1" AS tx_base_yr_en_lvl1,
    "TX_BASE_YR_FR_LVL1" AS tx_base_yr_fr_lvl1,
    "TX_BASE_YR_NL_LVL1" AS tx_base_yr_nl_lvl1,
    "TX_COICOP_DE_LVL1" AS tx_coicop_de_lvl1,
    "TX_COICOP_DE_LVL2" AS tx_coicop_de_lvl2,
    "TX_COICOP_DE_LVL3" AS tx_coicop_de_lvl3,
    "TX_COICOP_DE_LVL4" AS tx_coicop_de_lvl4,
    "TX_COICOP_DE_LVL5" AS tx_coicop_de_lvl5,
    "TX_COICOP_EN_LVL1" AS tx_coicop_en_lvl1,
    "TX_COICOP_EN_LVL2" AS tx_coicop_en_lvl2,
    "TX_COICOP_EN_LVL3" AS tx_coicop_en_lvl3,
    "TX_COICOP_EN_LVL4" AS tx_coicop_en_lvl4,
    "TX_COICOP_EN_LVL5" AS tx_coicop_en_lvl5,
    "TX_COICOP_FR_LVL1" AS tx_coicop_fr_lvl1,
    "TX_COICOP_FR_LVL2" AS tx_coicop_fr_lvl2,
    "TX_COICOP_FR_LVL3" AS tx_coicop_fr_lvl3,
    "TX_COICOP_FR_LVL4" AS tx_coicop_fr_lvl4,
    "TX_COICOP_FR_LVL5" AS tx_coicop_fr_lvl5,
    "TX_COICOP_NL_LVL1" AS tx_coicop_nl_lvl1,
    "TX_COICOP_NL_LVL2" AS tx_coicop_nl_lvl2,
    "TX_COICOP_NL_LVL3" AS tx_coicop_nl_lvl3,
    "TX_COICOP_NL_LVL4" AS tx_coicop_nl_lvl4,
    "TX_COICOP_NL_LVL5" AS tx_coicop_nl_lvl5,
    "CD_BASE_YR" AS cd_base_yr,
    "NM_CD_COICOP_LVL" AS nm_cd_coicop_lvl,
    "MS_IDX_HICP" AS ms_idx_hicp,
    "MS_IDX_HICP_CT" AS ms_idx_hicp_ct,
    "MS_WT_HICP" AS ms_wt_hicp,
    "MS_INFL_HICP" AS ms_infl_hicp,
    "MS_INFL_HICP_CT" AS ms_infl_hicp_ct,
    "NM_CD_BASE_YR_LVL" AS nm_cd_base_yr_lvl
FROM "statbel-nodeid4812"
