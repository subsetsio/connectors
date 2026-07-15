-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "assessed_income_group",
    "resident_type",
    "number_of_taxpayers",
    "assessable_income",
    "chargeable_income",
    "net_tax_assessed"
FROM "sg-data-d-f394f202534237671d39b17bd3b506ec"
