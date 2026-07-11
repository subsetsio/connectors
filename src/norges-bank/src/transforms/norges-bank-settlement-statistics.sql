-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "UNIT_MEASURE" AS unit_measure,
    "FREQ" AS freq,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "norges-bank-settlement-statistics"
