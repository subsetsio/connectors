-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "ADMINISTRATION: Administration" AS administration_administration,
    "EXPENDITURE: Expenditure" AS expenditure_expenditure,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_ADMINISTRATION_2: Note Administration 2" AS note_administration_2_note_administration_2,
    "NOTE_ADMINISTRATION_1: Note Administration 1" AS note_administration_1_note_administration_1,
    "NOTE_EXPENDITURE_2: Note Expenditure 2" AS note_expenditure_2_note_expenditure_2,
    "NOTE_EXPENDITURE_1: Note Expenditure 1" AS note_expenditure_1_note_expenditure_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-e2807"
