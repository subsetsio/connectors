-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "SEASONAL_ADJUST" AS seasonal_adjust,
    "SEX" AS sex,
    "FREQ" AS freq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "EP_MEASURE" AS ep_measure,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-pop-struct-series"
