-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "COMMENT_TS1: Detailed description of the group of series" AS comment_ts1_detailed_description_of_the_group_of_series,
    "COMMENT_TS: Detailed description of the group of series" AS comment_ts_detailed_description_of_the_group_of_series,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "DECIMALS: Decimals" AS decimals_decimals,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier
FROM "statec-df-a2109"
