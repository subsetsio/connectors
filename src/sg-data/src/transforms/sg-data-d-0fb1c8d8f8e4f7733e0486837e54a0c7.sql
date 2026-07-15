-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "no_of_indv_assessed",
    "total_income",
    "donations",
    "assessable_income"
FROM "sg-data-d-0fb1c8d8f8e4f7733e0486837e54a0c7"
