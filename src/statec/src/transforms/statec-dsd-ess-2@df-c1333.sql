-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "QUANTILE: Quantile" AS quantile_quantile,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "SEX: Sex" AS sex_sex,
    "ISCO08: Occupation (ISCO-08)" AS isco08_occupation_isco_08,
    "EDUC_LEVEL: Educational level" AS educ_level_educational_level,
    "RESIDENCE: Place of residence" AS residence_place_of_residence,
    "CPAYAGR: Collective labour agreement" AS cpayagr_collective_labour_agreement,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels
FROM "statec-dsd-ess-2@df-c1333"
