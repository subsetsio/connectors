-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "main_economic_activity_ar",
    "compensation_of_employees_qr_000_non_qatari",
    "compensation_of_employees_qr_000_qatari",
    "number_of_employees_non_qatari",
    "number_of_employees_qatari"
FROM "qatar-planning-and-statistics-authority-number-of-employees-and-estimates-of-compensation-of-employees-by-nationality-and-main-economic-activity"
