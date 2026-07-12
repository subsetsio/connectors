-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "number_of_employees",
    "compensations_of_employees_qr_000",
    "nationality",
    "main_economic_activity_ar",
    "nationality_ar"
FROM "qatar-planning-and-statistics-authority-number-of-employees-and-estimates-of-compensation-of-employees-by-nationality-and-main-economic-activity-activity-codes-53-5229-isic-rev4-10-or-more-employees"
