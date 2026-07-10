-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "TX_DESCR_NL" AS tx_descr_nl,
    "TX_DESCR_FR" AS tx_descr_fr,
    "CD_SECTOR" AS cd_sector,
    "TX_DESCR_SECTOR_NL" AS tx_descr_sector_nl,
    "TX_DESCR_SECTOR_FR" AS tx_descr_sector_fr,
    "DT_STRT_SECTOR" AS dt_strt_sector,
    "DT_STOP_SECTOR" AS dt_stop_sector,
    "MS_TOT_SUR" AS ms_tot_sur,
    CAST("POPULATION" AS BIGINT) AS population
FROM "statbel-nodeid2827"
