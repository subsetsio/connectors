-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "ENTERPRISES: Enterprises" AS enterprises_enterprises,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "NOTE_YEAR_2: Note" AS note_year_2_note,
    "NOTE_YEAR_1: Note" AS note_year_1_note,
    "NOTE_ENTERPRISES_2: Note" AS note_enterprises_2_note,
    "NOTE_ENTERPRISES_1: Note" AS note_enterprises_1_note
FROM "statec-df-d1500"
