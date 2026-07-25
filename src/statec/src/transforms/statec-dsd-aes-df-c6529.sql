-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "EDUC_ACTIVITY: Education activitity types" AS educ_activity_education_activitity_types,
    "RESULT: Result" AS result_result,
    "REASON: Reason" AS reason_reason,
    "ISCED-F2013: Fields of education and training" AS isced_f2013_fields_of_education_and_training,
    "AGE: Age class" AS age_age_class,
    "TRAINING: Training" AS training_training,
    "OCCUPATION_GROUP: Occupation" AS occupation_group_occupation,
    "WSTATUS: Labour status" AS wstatus_labour_status,
    "DEG_URB: Degree of urbanisation" AS deg_urb_degree_of_urbanisation,
    "EDUC_LEVEL: Educational level" AS educ_level_educational_level,
    "SEX: Sex" AS sex_sex,
    "FREQ: Frequency" AS freq_frequency,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "TIME_PERIOD: Time Period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "DECIMALS: Decimals" AS decimals_decimals,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier
FROM "statec-dsd-aes@df-c6529"
