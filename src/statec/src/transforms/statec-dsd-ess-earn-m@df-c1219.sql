-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "NACE_R2: Economic activity (NACE Rev.2)" AS nace_r2_economic_activity_nace_rev_2,
    "SEX: Sex" AS sex_sex,
    "SIZECLAS: Size class" AS sizeclas_size_class,
    "EDUC_LEVEL: Educational level" AS educ_level_educational_level,
    "ISCO08: International Standard Classification of Occupations 2008 (ISCO-08)" AS isco08_international_standard_classification_of_occupations_2008_isco_08,
    "RESID_STATUS: Residence status" AS resid_status_residence_status,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "COMMENT_OBS: Comments to the observation value" AS comment_obs_comments_to_the_observation_value,
    "COMMENT_TS: Detailed description of the group of series" AS comment_ts_detailed_description_of_the_group_of_series,
    "COMMENT_TS1: Detailed description of the group of series Nace R2" AS comment_ts1_detailed_description_of_the_group_of_series_nace_r2
FROM "statec-dsd-ess-earn-m@df-c1219"
