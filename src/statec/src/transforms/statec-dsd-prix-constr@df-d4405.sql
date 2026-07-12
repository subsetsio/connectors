-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE: Measure" AS measure_measure,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "FREQ: Frequency" AS freq_frequency,
    "MOTOR_ENERGY: Motor Energy" AS motor_energy_motor_energy,
    "COMMON_PRODUCT: Common products" AS common_product_common_products,
    "BASE_PERIOD: Base period" AS base_period_base_period,
    "CONSTR_TRADE: Construction trades" AS constr_trade_construction_trades,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "BUILDING_TYPE: Building type" AS building_type_building_type,
    "MARKET: Market" AS market_market,
    "PRODUCT_CPA_2_2: Products (CPA 2.2)" AS product_cpa_2_2_products_cpa_2_2,
    "TIME_TRANS: Time transformation" AS time_trans_time_transformation,
    "NRG_SRC: Energy source" AS nrg_src_energy_source,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "COMMENT_OBS: Comments to the observation value" AS comment_obs_comments_to_the_observation_value,
    "COMMENT_TS_CONSTR_TRADE: Detailed description of the group of series" AS comment_ts_constr_trade_detailed_description_of_the_group_of_series
FROM "statec-dsd-prix-constr@df-d4405"
