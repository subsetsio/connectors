-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO" AS geo,
    "SEASONAL_ADJUST" AS seasonal_adjust,
    CAST("BASE_PER" AS BIGINT) AS base_per,
    "PRODUCT_GROUP" AS product_group,
    "COICOP_2018" AS coicop_2018,
    "IDX_TYPE" AS idx_type,
    "TPH_CPI" AS tph_cpi,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "IND_TYPE" AS ind_type,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-ipc-princ"
