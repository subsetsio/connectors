-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "compensation_of_employees",
    "activity_code",
    "main_economic_activity_ar",
    "compensation_of_employees_ar",
    "value_qr"
FROM "qatar-planning-and-statistics-authority-number-of-employees-and-estimate-compensation-of-employees-by-nationality-and-main-economic-activity"
