-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "indicator",
    "nationality",
    "activity_code",
    "main_economic_activity_ar",
    "indicator_ar",
    "nationality_ar",
    "unit_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-employees-and-estimates-of-compensations-of-employees-by-nationality-and-main-economic-activity-2020-2021"
