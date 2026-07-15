-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "chargeable_income_group",
    "no_of_companies",
    "chargeable_income",
    "net_tax_assessed"
FROM "sg-data-d-093801b884a3fca429463cab981d6ccd"
