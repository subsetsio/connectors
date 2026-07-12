-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality",
    "nationality_ar",
    "gender",
    "gender_ar",
    "year",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-students-in-general-education-who-are-gcc-citizens-enrolled-in-government-schools-in-qatar1"
