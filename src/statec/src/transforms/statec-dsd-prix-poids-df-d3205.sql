-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE: Measure" AS measure_measure,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "FREQ: Frequency" AS freq_frequency,
    "BASE_PERIOD: Base period" AS base_period_base_period,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "MARKET: Market" AS market_market,
    "PRODUCT_CPA_2_2: Products (CPA 2.2)" AS product_cpa_2_2_products_cpa_2_2,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels
FROM "statec-dsd-prix-poids@df-d3205"
