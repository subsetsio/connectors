-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course",
    "enrolment"
FROM "sg-data-d-622fe07c9f187e565f61b5dfd15b5cac"
