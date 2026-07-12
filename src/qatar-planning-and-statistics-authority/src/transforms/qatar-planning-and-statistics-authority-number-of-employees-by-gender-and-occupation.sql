-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occupation",
    "employee_metric",
    "gender",
    "occupation_ar",
    "employee_metric_ar",
    "gender_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-employees-by-gender-and-occupation"
