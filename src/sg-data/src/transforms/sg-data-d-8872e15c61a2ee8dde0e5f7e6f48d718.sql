-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "residential_status",
    "long_term_unemployed"
FROM "sg-data-d-8872e15c61a2ee8dde0e5f7e6f48d718"
