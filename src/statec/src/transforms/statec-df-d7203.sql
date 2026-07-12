-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PRECIOUS_METALS: Precious metals" AS precious_metals_precious_metals,
    "PRICE: Price" AS price_price,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_PRICE_2: Note Price 2" AS note_price_2_note_price_2,
    "NOTE_PRICE_1: Note Price 1" AS note_price_1_note_price_1,
    "NOTE_PRECIOUS_METALS_2: Note Precious metals 1" AS note_precious_metals_2_note_precious_metals_1,
    "NOTE_PRECIOUS_METALS_1: Note Precious metals 2" AS note_precious_metals_1_note_precious_metals_2,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d7203"
