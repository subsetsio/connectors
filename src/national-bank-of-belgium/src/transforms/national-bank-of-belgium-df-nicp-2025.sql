-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "NBB_COICOP" AS nbb_coicop,
    CAST("INDEX_BASE" AS BIGINT) AS index_base,
    "INDEX_TYPE" AS index_type,
    "DERIVATION" AS derivation,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "OBS_STATUS" AS obs_status,
    "UNIT_MEASURE" AS unit_measure,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    CAST("DECIMALS" AS BIGINT) AS decimals
FROM "national-bank-of-belgium-df-nicp-2025"
