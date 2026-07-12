-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE: Measure" AS measure_measure,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "FREQ: Frequency" AS freq_frequency,
    "SEASONAL_ADJUST: Seasonal adjustment" AS seasonal_adjust_seasonal_adjustment,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "BASE_PER: Base period" AS base_per_base_period,
    "PRODUCT: Product" AS product_product,
    strptime("TIME_PERIOD: Time period", '%Y-%m')::DATE AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "CONF_STATUS: Confidential status" AS conf_status_confidential_status
FROM "statec-df-d5109"
