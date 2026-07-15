-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "category",
    "no_of_units"
FROM "sg-data-d-676bc7fa1d69de0e74c0ceb8897dcb10"
