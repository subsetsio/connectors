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
    "NOTE_QUARTER_2: Note quarter 2" AS note_quarter_2_note_quarter_2,
    "NOTE_QUARTER_1: Note quarter 1" AS note_quarter_1_note_quarter_1,
    "NOTE_PRICE_2: Note Price 2" AS note_price_2_note_price_2,
    "NOTE_PRICE_1: Note Price 1" AS note_price_1_note_price_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-a4504"
