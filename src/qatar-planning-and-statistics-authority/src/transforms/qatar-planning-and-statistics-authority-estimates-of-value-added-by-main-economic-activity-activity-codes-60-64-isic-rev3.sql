-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "economic_indicator",
    "component_of_economic_indicator",
    "main_economic_activity_ar",
    "economic_indicator_ar",
    "component_of_economic_indicator_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-estimates-of-value-added-by-main-economic-activity-activity-codes-60-64-isic-rev3"
