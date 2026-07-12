-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "nationality",
    "sex",
    "main_economic_activity_ar",
    "nationality_ar",
    "sex_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-employees-by-sex-nationality-and-main-economic-activity-transport-and-communication-statistics-less"
