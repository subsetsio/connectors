-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cbo_name",
    "program_id",
    "_name" AS name,
    "fiscal_year",
    "amount"
FROM "nyc-open-data-75e9-fg2t"
