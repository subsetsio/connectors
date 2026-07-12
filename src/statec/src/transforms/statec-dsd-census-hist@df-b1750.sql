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
    "CITIZEN: Citizenship" AS citizen_citizenship,
    "AGE: Age class" AS age_age_class,
    "C_BIRTH: Country of birth" AS c_birth_country_of_birth,
    "SIZE_PRV_HH: Size of household" AS size_prv_hh_size_of_household,
    "TSH: Tenure status of household" AS tsh_tenure_status_of_household,
    "LMS: Legal marital status" AS lms_legal_marital_status,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-dsd-census-hist@df-b1750"
