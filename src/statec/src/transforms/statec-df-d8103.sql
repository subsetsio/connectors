-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "STAFF: Staff" AS staff_staff,
    "SECTOR: Sector" AS sector_sector,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_STAFF_2: NoteStaff 2" AS note_staff_2_notestaff_2,
    "NOTE_STAFF_1: Note Staff 1" AS note_staff_1_note_staff_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_SECTOR_2: Note sector 2" AS note_sector_2_note_sector_2,
    "NOTE_SECTOR_1: Note secteur 1" AS note_sector_1_note_secteur_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d8103"
