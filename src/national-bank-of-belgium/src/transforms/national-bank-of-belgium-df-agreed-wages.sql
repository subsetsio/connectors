-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "WORKER_CATEGORY" AS worker_category,
    CAST("INDEX_BASE" AS BIGINT) AS index_base,
    "INDEX_TYPE" AS index_type,
    "DERIVATION" AS derivation,
    "WAGES_SECTOR" AS wages_sector,
    "ADJUSTMENT" AS adjustment,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "OBS_STATUS" AS obs_status,
    "UNIT_MEASURE" AS unit_measure,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "COMPILING_ORG" AS compiling_org,
    "EMBARGO_TIME" AS embargo_time,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "CONF_STATUS" AS conf_status
FROM "national-bank-of-belgium-df-agreed-wages"
