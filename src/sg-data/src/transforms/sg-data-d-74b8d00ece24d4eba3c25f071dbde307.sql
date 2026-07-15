-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_name",
    "course_description",
    "reference"
FROM "sg-data-d-74b8d00ece24d4eba3c25f071dbde307"
