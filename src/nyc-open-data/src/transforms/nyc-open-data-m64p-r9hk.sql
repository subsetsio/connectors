-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "last_name",
    "first_name",
    "certification_number",
    "expiration_date",
    "telephone"
FROM "nyc-open-data-m64p-r9hk"
