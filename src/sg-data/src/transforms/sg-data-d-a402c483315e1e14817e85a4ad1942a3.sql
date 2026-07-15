-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_name",
    "course_description",
    "reference"
FROM "sg-data-d-a402c483315e1e14817e85a4ad1942a3"
