-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "MUNICIPALITIES: Municipalities" AS municipalities_municipalities,
    "CLASS: Class" AS class_class,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_MUNICIPALITIES_2: Note Municipalities 2" AS note_municipalities_2_note_municipalities_2,
    "NOTE_MUNICIPALITIES_1: Note Municipalities 1" AS note_municipalities_1_note_municipalities_1,
    "NOTE_CLASS_2: Note Class 2" AS note_class_2_note_class_2,
    "NOTE_CLASS_1: Note Class 1" AS note_class_1_note_class_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-x011"
