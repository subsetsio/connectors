-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "field_of_training_ar",
    "field_of_training",
    "nationality_ar",
    "nationality",
    "educational_status_ar",
    "educational_status",
    "gender_ar",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-trainees-at-the-private-training-centers-according-to-the-educational-status-gender-nationality-and"
