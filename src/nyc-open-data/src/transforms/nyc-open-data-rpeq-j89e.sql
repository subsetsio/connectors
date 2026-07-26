-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dca_license_number",
    "business_name",
    "business_name_2",
    "industry",
    "event_type",
    "event_date",
    "status"
FROM "nyc-open-data-rpeq-j89e"
