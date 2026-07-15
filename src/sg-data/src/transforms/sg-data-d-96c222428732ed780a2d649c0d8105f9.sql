-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "tax_group",
    "no_of_indv_assessed",
    "total_income",
    "donations",
    "assessable_income"
FROM "sg-data-d-96c222428732ed780a2d649c0d8105f9"
