-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Scholarship_and_Awards" AS scholarship_and_awards,
    "Description" AS description,
    "Reference" AS reference
FROM "sg-data-d-d8f0c6d636374b50c5565c5c2d1bd1ea"
