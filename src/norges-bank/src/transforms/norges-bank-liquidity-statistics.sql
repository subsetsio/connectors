-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "LIQUIDITY_MAIN" AS liquidity_main,
    "LIQUIDITY_DETAILS" AS liquidity_details,
    "UNIT_MEASURE" AS unit_measure,
    "INSTRUMENT_TYPE" AS instrument_type,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "norges-bank-liquidity-statistics"
