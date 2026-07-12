-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "EMPLOYEES: Employees" AS employees_employees,
    "ACTIVITY: Activity" AS activity_activity,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_EMPLOYEES_2: Note Employees 2" AS note_employees_2_note_employees_2,
    "NOTE_EMPLOYEES_1: Note Employees 1" AS note_employees_1_note_employees_1,
    "NOTE_ACTIVITY_2: Note Activity 2" AS note_activity_2_note_activity_2,
    "NOTE_ACTIVITY_1: Note Activity 1" AS note_activity_1_note_activity_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d8350"
