-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_category",
    "no_of_classes"
FROM "sg-data-d-80ece7b4cf25e843592ef0431f96f6e2"
