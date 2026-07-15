-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "tax_type",
    "return_type",
    "no_of_returns"
FROM "sg-data-d-76a34b1f7e0f9e5412ee8829183182d4"
