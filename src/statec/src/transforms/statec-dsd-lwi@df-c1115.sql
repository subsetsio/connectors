-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "SEX: Sex" AS sex_sex,
    "AGE: Age class" AS age_age_class,
    "ISCED11: Level of education" AS isced11_level_of_education,
    "CITIZEN: Citizenship" AS citizen_citizenship,
    "C_BIRTH: Country of birth" AS c_birth_country_of_birth,
    "WSTATUS: Working status" AS wstatus_working_status,
    "QUANTILE: Quantile" AS quantile_quantile,
    "FREQ: Frequency" AS freq_frequency,
    "MEASURE: Measure" AS measure_measure,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "COMMENT_OBS: Comments to the observation value" AS comment_obs_comments_to_the_observation_value,
    "COMMENT_TS: Detailed description of the group of series" AS comment_ts_detailed_description_of_the_group_of_series,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-dsd-lwi@df-c1115"
