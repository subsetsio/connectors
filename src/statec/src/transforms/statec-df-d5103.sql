-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "CANTON: Canton" AS canton_canton,
    "SECTOR: Sector" AS sector_sector,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_CANTON_2: Note Canton 2" AS note_canton_2_note_canton_2,
    "NOTE_CANTON_1: Note Canton 1" AS note_canton_1_note_canton_1,
    "NOTE_SECTOR_2: Note Sector 2" AS note_sector_2_note_sector_2,
    "NOTE_SECTOR_1: Note Sector 1" AS note_sector_1_note_sector_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d5103"
