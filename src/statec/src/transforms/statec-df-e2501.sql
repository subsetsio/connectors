-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "LABELS: Labels" AS labels_labels,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_QUARTERS_2: Note quarter 2" AS note_quarters_2_note_quarter_2,
    "NOTE_QUARTERS_1: Note quarter 1" AS note_quarters_1_note_quarter_1,
    "NOTE_LABELS_2: Note Labels 2" AS note_labels_2_note_labels_2,
    "NOTE_LABELS_1: Note Labels 1" AS note_labels_1_note_labels_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-e2501"
