-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "type",
    "status",
    "no_of_units"
FROM "sg-data-d-4b69ac0ff084e96f03197ad346248918"
