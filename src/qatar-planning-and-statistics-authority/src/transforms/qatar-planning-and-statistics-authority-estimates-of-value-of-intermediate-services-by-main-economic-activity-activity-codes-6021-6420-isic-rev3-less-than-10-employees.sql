-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "intermediate_services",
    "value",
    "main_economic_activity_ar",
    "intermediate_services_ar"
FROM "qatar-planning-and-statistics-authority-estimates-of-value-of-intermediate-services-by-main-economic-activity-activity-codes-6021-6420-isic-rev3-less-than-10-employees"
