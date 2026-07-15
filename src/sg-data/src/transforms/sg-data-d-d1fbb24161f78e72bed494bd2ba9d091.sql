-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "nmc_course_level",
    "training_places"
FROM "sg-data-d-d1fbb24161f78e72bed494bd2ba9d091"
