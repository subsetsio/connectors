-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no._of_new_applications" AS no_of_new_applications,
    "no._of_variation" AS no_of_variation
FROM "sg-data-d-174e3fa410a13a1eeb70b0c4513d8b86"
