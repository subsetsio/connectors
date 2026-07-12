-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "LABELS: Labels" AS labels_labels,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_YEARS_2: Note years 2" AS note_years_2_note_years_2,
    "NOTE_YEARS_1: Note years 1" AS note_years_1_note_years_1,
    "NOTE_LABELS_2: Note Labels 2" AS note_labels_2_note_labels_2,
    "NOTE_LABELS_1: Note Labels 1" AS note_labels_1_note_labels_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-e3302"
