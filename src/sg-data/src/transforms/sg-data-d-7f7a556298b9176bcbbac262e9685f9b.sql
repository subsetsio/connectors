-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "assessed_income_group",
    "no_of_companies",
    "assessable_income",
    "net_tax_assessed"
FROM "sg-data-d-7f7a556298b9176bcbbac262e9685f9b"
