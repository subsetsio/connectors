-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "SEX: Sex" AS sex_sex,
    "AGE: Age" AS age_age,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_SEX_2: Note sex 2" AS note_sex_2_note_sex_2,
    "NOTE_SEX_1: Note sex 1" AS note_sex_1_note_sex_1,
    "NOTE_AGE_2: Note Age 2" AS note_age_2_note_age_2,
    "NOTE_AGE_1: Note Age 1" AS note_age_1_note_age_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-b2209"
