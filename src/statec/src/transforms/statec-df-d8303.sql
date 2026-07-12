-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "ENTERPRISES: Enterprises" AS enterprises_enterprises,
    "SPECIFICATION: Specification" AS specification_specification,
    "YEARS: Years" AS years_years,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_ENTERPRISES_2: Note Enterprises 2" AS note_enterprises_2_note_enterprises_2,
    "NOTE_ENTERPRISES_1: Note Enterprises 1" AS note_enterprises_1_note_enterprises_1,
    "NOTE_SPECIFICATION_2: Note specification 2" AS note_specification_2_note_specification_2,
    "NOTE_SPECIFICATION_1: Note specification 1" AS note_specification_1_note_specification_1,
    "NOTE_YEARS_2: Note years 2" AS note_years_2_note_years_2,
    "NOTE_YEARS_1: Note years 1" AS note_years_1_note_years_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d8303"
