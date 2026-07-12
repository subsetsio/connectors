-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "GEOPOLITIC: Geopolitic" AS geopolitic_geopolitic,
    "SPECIFICATION: Specification" AS specification_specification,
    "CLASSIFICATION: Classification" AS classification_classification,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_GEOPOLITIC_2: Note Geopolitic 2" AS note_geopolitic_2_note_geopolitic_2,
    "NOTE_GEOPOLITIC_1: Note Geopolitic 1" AS note_geopolitic_1_note_geopolitic_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_SPECIFICATION_2: Note specification 2" AS note_specification_2_note_specification_2,
    "NOTE_SPECIFICATION_1: Note specification 1" AS note_specification_1_note_specification_1,
    "NOTE_CLASSIFICATION_2: Note classification 2" AS note_classification_2_note_classification_2,
    "NOTE_CLASSIFICATION_1: Note classification 1" AS note_classification_1_note_classification_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-e2801"
