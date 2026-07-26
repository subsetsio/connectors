-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "trust_name",
    "donation_name",
    "description",
    "amount",
    "date_of_donation",
    "first_name",
    "last_name",
    "city",
    "state",
    "zip_code"
FROM "nyc-open-data-jsiv-zh9r"
