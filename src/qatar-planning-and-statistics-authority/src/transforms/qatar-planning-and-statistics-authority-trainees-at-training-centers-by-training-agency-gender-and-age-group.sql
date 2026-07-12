-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_groups_in_years",
    "age_groups_in_years_ar",
    "govt_corporations_males",
    "govt_corporations_females",
    "mixed_training_centers_males",
    "mixed_training_centers_females",
    "private_training_centers_males",
    "private_training_centers_females"
FROM "qatar-planning-and-statistics-authority-trainees-at-training-centers-by-training-agency-gender-and-age-group"
