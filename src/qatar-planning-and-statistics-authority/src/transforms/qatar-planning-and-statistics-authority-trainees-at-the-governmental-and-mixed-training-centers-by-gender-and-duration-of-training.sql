-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "duration_of_training_ar",
    "duration_of_training",
    "training_agency_ar",
    "training_agency",
    "gender_ar",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-trainees-at-the-governmental-and-mixed-training-centers-by-gender-and-duration-of-training"
