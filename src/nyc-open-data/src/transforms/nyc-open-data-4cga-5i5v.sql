-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_day" AS day,
    "borough",
    "swimming_pool",
    "program_type",
    "male_registration",
    "female_registration",
    "total_registration",
    "male_attendance",
    "female_attendance",
    "total_attendance"
FROM "nyc-open-data-4cga-5i5v"
