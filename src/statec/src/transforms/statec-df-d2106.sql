-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PRODUCTION: Production" AS production_production,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_PROD2: Note production" AS note_prod2_note_production,
    "NOTE_PROD1: Note production" AS note_prod1_note_production,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d2106"
