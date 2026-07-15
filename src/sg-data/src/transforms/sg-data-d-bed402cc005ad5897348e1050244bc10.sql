-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "resident_type",
    "chargeable_income_group",
    "no_of_companies",
    "chargeable_income",
    "net_tax_assessed"
FROM "sg-data-d-bed402cc005ad5897348e1050244bc10"
