-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SEASONAL_ADJUST" AS seasonal_adjust,
    CAST("BASE_PER" AS BIGINT) AS base_per,
    "IDX_TYPE" AS idx_type,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-coeff-euro-franc"
