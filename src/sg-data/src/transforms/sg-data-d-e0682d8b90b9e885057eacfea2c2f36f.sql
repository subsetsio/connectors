-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_ref_no",
    "course_title"
FROM "sg-data-d-e0682d8b90b9e885057eacfea2c2f36f"
