-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school",
    "course_type",
    "course_name",
    "gender",
    "count"
FROM "sg-data-d-47c5df883c38077cf5b432162af51056"
