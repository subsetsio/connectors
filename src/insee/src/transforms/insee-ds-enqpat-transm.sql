-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PCS" AS pcs,
    "AMOUNT_SIZE" AS amount_size,
    "NAT_AIDE" AS nat_aide,
    "TRANSM_TYPE" AS transm_type,
    "GEO" AS geo,
    "QUANTILE" AS quantile,
    "PERIOD_AIDE" AS period_aide,
    "QUANTILE_MEASURE" AS quantile_measure,
    "ENQPAT_MEASURE" AS enqpat_measure,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "NAT_HER_DON" AS nat_her_don,
    "PERS_ORIG_TRANSM" AS pers_orig_transm,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-enqpat-transm"
