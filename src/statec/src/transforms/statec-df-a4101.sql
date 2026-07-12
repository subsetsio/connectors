-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PRODUCT: Product" AS product_product,
    "FREQ: Frequency" AS freq_frequency,
    strptime("TIME_PERIOD: Time period", '%Y-%m')::DATE AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "NOTE_PRODUCT_2: Note Product 2" AS note_product_2_note_product_2,
    "NOTE_PRODUCT_1: Note Product 1" AS note_product_1_note_product_1,
    "NOTE_MONTH_2: Note Month 2" AS note_month_2_note_month_2,
    "NOTE_MONTH_1: Note Month 1" AS note_month_1_note_month_1
FROM "statec-df-a4101"
