-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "REF_AREA" AS ref_area,
    "IND_TYPE" AS ind_type,
    "IDX_TYPE" AS idx_type,
    CAST("BASE_PER" AS BIGINT) AS base_per,
    "ITEM" AS item,
    "COVERAGE_GEO" AS coverage_geo,
    "COVERAGE_POP" AS coverage_pop,
    "SEASONAL_ADJUST" AS seasonal_adjust,
    "TRANSFORMATION" AS transformation,
    "CUST_BREAKDOWN" AS cust_breakdown,
    "UNIT_MEASURE" AS unit_measure,
    "TIME_FORMAT" AS time_format,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    strptime("TIME_PERIOD", '%Y-%m')::DATE AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "CONF_STATUS" AS conf_status,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "OBS_STATUS" AS obs_status
FROM "ksh-3cc11704-5617-446b-ad92-d74c0c081cec"
