-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "intermediate_services",
    "main_economic_activity_ar",
    "intermediate_services_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-estimates-of-value-of-intermediate-services-by-main-economic-activity-activity-codes-53-5229-isic-rev4"
