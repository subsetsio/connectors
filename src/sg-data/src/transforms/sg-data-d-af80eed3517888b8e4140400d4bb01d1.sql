-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "institution",
    "mode",
    "sex",
    "enrolment",
    "teaching_staff"
FROM "sg-data-d-af80eed3517888b8e4140400d4bb01d1"
