-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "economic_sector",
    "no_of_companies",
    "assessable_income",
    "chargeable_income",
    "net_tax_assessed"
FROM "sg-data-d-c4acab391625845ab55673166c614001"
