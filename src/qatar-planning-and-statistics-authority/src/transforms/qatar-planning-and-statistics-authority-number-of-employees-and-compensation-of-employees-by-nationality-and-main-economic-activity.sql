-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "main_economic_activity_ar",
    "economic_activity",
    "economic_activity_ar",
    "labor_indicator",
    "labor_indicator_ar",
    "nationality",
    "nationality_ar",
    "code",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-employees-and-compensation-of-employees-by-nationality-and-main-economic-activity"
