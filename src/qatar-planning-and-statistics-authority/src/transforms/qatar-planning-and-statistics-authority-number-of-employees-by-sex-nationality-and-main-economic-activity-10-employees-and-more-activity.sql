-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "nationality",
    "gender",
    "no_of_employees",
    "main_economic_activity_ar",
    "nationality_ar",
    "gender_ar"
FROM "qatar-planning-and-statistics-authority-number-of-employees-by-sex-nationality-and-main-economic-activity-10-employees-and-more-activity"
