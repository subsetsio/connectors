-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "POP_MOVEMENT: Population Movement" AS pop_movement_population_movement,
    "CANTON: Canton" AS canton_canton,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_POP_MOVEMENT_2: Note Population Movement 2" AS note_pop_movement_2_note_population_movement_2,
    "NOTE_POP_MOVEMENT_1: Note Population Movement 1" AS note_pop_movement_1_note_population_movement_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_CANTON_2: Note canton 2" AS note_canton_2_note_canton_2,
    "NOTE_CANTON_1: Note canton 1" AS note_canton_1_note_canton_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-x025"
