-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_category",
    "no_of_participants"
FROM "sg-data-d-ad1036159bf22ebfc6d1425175701ea7"
