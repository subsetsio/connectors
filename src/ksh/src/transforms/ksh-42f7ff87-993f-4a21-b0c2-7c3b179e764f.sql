-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "REF_AREA" AS ref_area,
    "SEASONAL_ADJUST" AS seasonal_adjust,
    "INDICATOR" AS indicator,
    "ACTIVITY" AS activity,
    CAST("BASE_PER" AS BIGINT) AS base_per,
    "PRODUCT" AS product,
    "TRANSFORMATION" AS transformation,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "UNIT_MEASURE" AS unit_measure,
    "TIME_FORMAT" AS time_format,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "OBS_STATUS" AS obs_status,
    "CONF_STATUS" AS conf_status,
    "EMBARGO_TIME" AS embargo_time
FROM "ksh-42f7ff87-993f-4a21-b0c2-7c3b179e764f"
