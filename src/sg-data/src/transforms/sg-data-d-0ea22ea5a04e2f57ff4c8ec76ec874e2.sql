-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_name",
    "course_description",
    "reference"
FROM "sg-data-d-0ea22ea5a04e2f57ff4c8ec76ec874e2"
