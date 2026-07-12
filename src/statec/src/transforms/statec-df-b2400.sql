-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "SEX: Sex" AS sex_sex,
    "POP_MOVEMENT: Pop. movement" AS pop_movement_pop_movement,
    "SPECIFICATION: Specification" AS specification_specification,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_SEX_2: Note sex 2" AS note_sex_2_note_sex_2,
    "NOTE_SEX_1: Note sex 1" AS note_sex_1_note_sex_1,
    "NOTE_POP_MOVEMENT_2: Note Pop. movement 2" AS note_pop_movement_2_note_pop_movement_2,
    "NOTE_POP_MOVEMENT_1: Note Pop. movement 1" AS note_pop_movement_1_note_pop_movement_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_SPECIFICATION_2: Note specification 2" AS note_specification_2_note_specification_2,
    "NOTE_SPECIFICATION_1: Note specification 1" AS note_specification_1_note_specification_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-b2400"
