-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grant_call",
    "closing_date",
    "total_grants_awarded"
FROM "sg-data-d-c53ee81929822a5aad1a41f8415ceb0c"
