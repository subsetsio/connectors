-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "main_economic_activity_ar",
    "establishments_with_10_employee_emp",
    "establishments_with_10_employee_estb",
    "establishments_with_10_employee_emp0",
    "establishments_with_10_employee_estb0"
FROM "qatar-planning-and-statistics-authority-number-of-establishments-and-employees-by-size-of-establishment-and-main-economic-activity0"
