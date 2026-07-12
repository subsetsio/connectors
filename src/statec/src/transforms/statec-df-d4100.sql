-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PERMIT: Permit" AS permit_permit,
    "VARIABLE: Variable" AS variable_variable,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_PERMIT_2: Note Permit 2" AS note_permit_2_note_permit_2,
    "NOTE_PERMIT_1: Note Permit 1" AS note_permit_1_note_permit_1,
    "NOTE_VARIABLE_2: Note Variable 2" AS note_variable_2_note_variable_2,
    "NOTE_VARIABLE_1: Note Variable 1" AS note_variable_1_note_variable_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1
FROM "statec-df-d4100"
