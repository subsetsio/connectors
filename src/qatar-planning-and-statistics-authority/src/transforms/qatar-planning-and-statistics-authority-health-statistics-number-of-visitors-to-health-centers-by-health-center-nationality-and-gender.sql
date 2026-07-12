-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "health_center",
    "health_center_ar",
    "nationality",
    "nationality_ar",
    "gender",
    "gender_ar",
    "number_of_visitors"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-visitors-to-health-centers-by-health-center-nationality-and-gender"
