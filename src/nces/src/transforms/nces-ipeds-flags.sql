-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    CAST("STAT_IC" AS BIGINT) AS stat_ic,
    CAST("LOCK_IC" AS BIGINT) AS lock_ic,
    CAST("IMP_IC" AS BIGINT) AS imp_ic,
    CAST("STAT_C" AS BIGINT) AS stat_c,
    CAST("LOCK_C" AS BIGINT) AS lock_c,
    CAST("PRCH_C" AS BIGINT) AS prch_c,
    CAST("IDX_C" AS BIGINT) AS idx_c,
    "PCC_F" AS pcc_f,
    CAST("IMP_C" AS BIGINT) AS imp_c,
    "STAT_E12" AS stat_e12,
    "LOCK_E12" AS lock_e12,
    "PRCH_E12" AS prch_e12,
    "IDX_E12" AS idx_e12,
    "PCE12_F" AS pce12_f,
    "IMP_E12" AS imp_e12,
    "year"
FROM "nces-ipeds-flags"
