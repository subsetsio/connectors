-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "chargeable_income_group",
    "resident_type",
    "number_of_taxpayers",
    "assessable_income",
    "chargeable_income",
    "net_tax_assessed"
FROM "sg-data-d-81675d7bbd87f3ffe8ad3b8db67399e5"
