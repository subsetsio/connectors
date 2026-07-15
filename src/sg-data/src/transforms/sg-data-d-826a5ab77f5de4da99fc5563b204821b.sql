-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "tax_type",
    "arrears_type",
    "tax_arrears"
FROM "sg-data-d-826a5ab77f5de4da99fc5563b204821b"
