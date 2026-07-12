-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "main_economic_indicator",
    "sub_indicator",
    "main_economic_activity_ar",
    "main_economic_indicator_ar",
    "sub_indicator_ar",
    "lwhd_unit",
    "value"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-by-main-economic-activity-activity-codes-49-61-isic-rev4"
