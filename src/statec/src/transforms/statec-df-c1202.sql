-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "NACE_REV2: NACE Rev.2" AS nace_rev2_nace_rev_2,
    "GENDER: Gender" AS gender_gender,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_NACE_REV2_2: Note NACE Rev.2_2" AS note_nace_rev2_2_note_nace_rev_2_2,
    "NOTE_NACE_REV2_1: Note NACE Rev.2_1" AS note_nace_rev2_1_note_nace_rev_2_1,
    "NOTE_GENDER_2: Note Gender 2" AS note_gender_2_note_gender_2,
    "NOTE_GENDER_1: Note Gender 1" AS note_gender_1_note_gender_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Décimales" AS decimals_d_cimales
FROM "statec-df-c1202"
