-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "BUDGET_COMPONENT: Consumption basket" AS budget_component_consumption_basket,
    "HHCOMP: Household composition" AS hhcomp_household_composition,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "COMMENT_OBS: Comments to the observation value" AS comment_obs_comments_to_the_observation_value,
    "COMMENT_TS_HHCOMP: Detailed description of the group of series household composition" AS comment_ts_hhcomp_detailed_description_of_the_group_of_series_household_composition,
    "COMMENT_TS_BUDGET_COMPONENT: Detailed description of the group of series budget component" AS comment_ts_budget_component_detailed_description_of_the_group_of_series_budget_component
FROM "statec-dsd-budget-ref@df-c1501"
