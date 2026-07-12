-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "ACTIVITY: Activity" AS activity_activity,
    "CODE: Code" AS code_code,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_ACTIVITY_2: Note Activity 2" AS note_activity_2_note_activity_2,
    "NOTE_ACTIVITY_1: Note Activity 1" AS note_activity_1_note_activity_1,
    "NOTE_CODE_2: Note Code 2" AS note_code_2_note_code_2,
    "NOTE_CODE_1: Note Code 1" AS note_code_1_note_code_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d8364"
