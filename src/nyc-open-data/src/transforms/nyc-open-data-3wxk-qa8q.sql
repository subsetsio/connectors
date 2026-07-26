-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kit_id_number",
    "borough",
    "zipcode",
    "date_collected",
    "received_date",
    "first_draw_atthetap_lead_level_gl",
    "first_draw_atthetap_copper_level_mgl"
FROM "nyc-open-data-3wxk-qa8q"
