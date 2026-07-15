-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_ref",
    "course_title"
FROM "sg-data-d-bd01bb6b241f2bd0173aea1fd31ac615"
