-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "CD_SECTOR" AS cd_sector,
    CAST("TOTAL" AS BIGINT) AS total,
    "DT_STRT_SECTOR" AS dt_strt_sector,
    "DT_STOP_SECTOR" AS dt_stop_sector,
    "OPPERVLAKKTE_IN_HM" AS oppervlakkte_in_hm,
    "TX_DESCR_SECTOR_NL" AS tx_descr_sector_nl,
    "TX_DESCR_SECTOR_FR" AS tx_descr_sector_fr,
    "TX_DESCR_NL" AS tx_descr_nl,
    "TX_DESCR_FR" AS tx_descr_fr
FROM "statbel-nodeid4796"
