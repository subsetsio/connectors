-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "SIZE_EMP: Employment size class" AS size_emp_employment_size_class,
    "NACE_REV_20: NACE Rev.2" AS nace_rev_20_nace_rev_2,
    "INDICATOR: Indicator" AS indicator_indicator,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_INDICATOR: Note to the indicator" AS note_indicator_note_to_the_indicator,
    "UNIT: Measurement unit" AS unit_measurement_unit,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d1115"
