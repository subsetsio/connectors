-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "entity_type",
    "no_of_businesses"
FROM "sg-data-d-b6cde411e2fa7098022a0e787fc99c90"
