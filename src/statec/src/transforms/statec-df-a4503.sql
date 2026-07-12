-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PRICE: Price" AS price_price,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_SEMESTER_2: Note semester 2" AS note_semester_2_note_semester_2,
    "NOTE_SEMESTER_1: Note semester 1" AS note_semester_1_note_semester_1,
    "NOTE_PRICE_2: Note Price 2" AS note_price_2_note_price_2,
    "NOTE_PRICE_1: Note Price 1" AS note_price_1_note_price_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-a4503"
