-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "ECHELON: Echelon" AS echelon_echelon,
    "GRADE: Grade" AS grade_grade,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_ECHELON_2: Note Echelon 2" AS note_echelon_2_note_echelon_2,
    "NOTE_ECHELON_1: Note Echelon 1" AS note_echelon_1_note_echelon_1,
    "NOTE_GRADE_2: Note Grade 2" AS note_grade_2_note_grade_2,
    "NOTE_GRADE_1: Note Grade 1" AS note_grade_1_note_grade_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-c1251"
