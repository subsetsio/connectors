-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "nature_of_employment",
    "total_paid_hours",
    "standard_hours"
FROM "sg-data-d-ce1286635541b65ec31c7c9d43044737"
