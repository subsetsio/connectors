-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "no_of_complaints_handled",
    "financial_year"
FROM "sg-data-d-59e7a1bc31a51c1475ef1484c03faf33"
