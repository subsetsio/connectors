-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SEASONAL_ADJUST" AS seasonal_adjust,
    CAST("BASE_PER" AS BIGINT) AS base_per,
    "IDX_TYPE" AS idx_type,
    "INDICATOR" AS indicator,
    "FREQ" AS freq,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    "MARCHE" AS marche,
    "ACTIVITY" AS activity,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-ica"
