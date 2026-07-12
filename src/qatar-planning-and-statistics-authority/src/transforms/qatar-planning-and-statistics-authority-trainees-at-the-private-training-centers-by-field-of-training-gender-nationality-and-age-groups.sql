-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_groups_in_years_ar",
    "age_groups",
    "nationality_ar",
    "nationality",
    "field_of_training_ar",
    "field_of_training",
    "gender_ar",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-trainees-at-the-private-training-centers-by-field-of-training-gender-nationality-and-age-groups"
