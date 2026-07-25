-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "SEX: Sex" AS sex_sex,
    "AGE_CLASS: Age" AS age_class_age,
    "DURATION: Marriage duration" AS duration_marriage_duration,
    "N_CHILD: Minor children" AS n_child_minor_children,
    "CAUSE: Reason for divorce" AS cause_reason_for_divorce,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels
FROM "statec-dsd-divorces@df-b2603"
