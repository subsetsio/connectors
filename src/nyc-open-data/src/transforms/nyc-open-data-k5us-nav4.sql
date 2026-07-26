-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kit_id",
    "borough",
    "zipcode",
    "date_collected",
    "date_received",
    "lead_first_draw_mgl",
    "lead_12_minute_flush_mgl",
    "lead_5_minute_flush_mgl",
    "copper_first_draw_mgl",
    "copper_12_minute_flush_mgl",
    "copper_5_minute_flush_mgl"
FROM "nyc-open-data-k5us-nav4"
