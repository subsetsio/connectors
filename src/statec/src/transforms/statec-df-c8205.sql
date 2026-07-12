-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "DISCIPLINE: Discipline" AS discipline_discipline,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_DISCIPLINE_2: Note Discipline 2" AS note_discipline_2_note_discipline_2,
    "NOTE_DISCIPLINE_1: Note Discipline 1" AS note_discipline_1_note_discipline_1
FROM "statec-df-c8205"
