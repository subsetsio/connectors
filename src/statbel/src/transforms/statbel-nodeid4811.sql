-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NM_YR" AS BIGINT) AS nm_yr,
    CAST("NM_MTH" AS BIGINT) AS nm_mth,
    "CD_COICOP_AGGR" AS cd_coicop_aggr,
    "TX_BASE_YR_DE_LVL1" AS tx_base_yr_de_lvl1,
    "TX_BASE_YR_EN_LVL1" AS tx_base_yr_en_lvl1,
    "TX_BASE_YR_FR_LVL1" AS tx_base_yr_fr_lvl1,
    "TX_BASE_YR_NL_LVL1" AS tx_base_yr_nl_lvl1,
    "TX_COICOP_AGGR_DE_LVL1" AS tx_coicop_aggr_de_lvl1,
    "TX_COICOP_AGGR_EN_LVL1" AS tx_coicop_aggr_en_lvl1,
    "TX_COICOP_AGGR_FR_LVL1" AS tx_coicop_aggr_fr_lvl1,
    "TX_COICOP_AGGR_NL_LVL1" AS tx_coicop_aggr_nl_lvl1,
    "TX_COICOP_DE_LVL1" AS tx_coicop_de_lvl1,
    "TX_COICOP_DE_LVL2" AS tx_coicop_de_lvl2,
    "TX_COICOP_DE_LVL3" AS tx_coicop_de_lvl3,
    "TX_COICOP_DE_LVL4" AS tx_coicop_de_lvl4,
    "TX_COICOP_DE_LVL5" AS tx_coicop_de_lvl5,
    "CD_COICOP" AS cd_coicop,
    "CD_BASE_YR" AS cd_base_yr,
    CAST("NM_CD_COICOP_LVL" AS BIGINT) AS nm_cd_coicop_lvl,
    CAST("MS_IDX_HICP" AS DOUBLE) AS ms_idx_hicp,
    CAST("MS_WT_HICP" AS DOUBLE) AS ms_wt_hicp,
    "MS_INFL_HICP" AS ms_infl_hicp,
    CAST("NM_CD_BASE_YR_LVL" AS BIGINT) AS nm_cd_base_yr_lvl
FROM "statbel-nodeid4811"
