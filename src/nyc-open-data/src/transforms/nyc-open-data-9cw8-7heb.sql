-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "domain_name",
    "domain_registration_date",
    "nexus_category"
FROM "nyc-open-data-9cw8-7heb"
