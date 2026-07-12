-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "HUSBAND_2: Husband 2" AS husband_2_husband_2,
    "HUSBAND_1: Husband 1" AS husband_1_husband_1,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "NOTE_HUSBAND_2_2: Note 2 Husband 2" AS note_husband_2_2_note_2_husband_2,
    "NOTE_HUSBAND_2_1: Note 1 Husband 2" AS note_husband_2_1_note_1_husband_2,
    "NOTE_HUSBAND_1_2: Note 2 Husband 1" AS note_husband_1_2_note_2_husband_1,
    "NOTE_HUSBAND_1_1: Note 1 Husband 1" AS note_husband_1_1_note_1_husband_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1
FROM "statec-df-b2506"
