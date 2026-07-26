-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "timestamp",
    "last_name",
    "first_name",
    "organization",
    "what_type_of_request_is_this"
FROM "nyc-open-data-gqzy-vhwd"
