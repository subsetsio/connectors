-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "economic_indicator_name",
    "economic_indicator_category",
    "activity_code",
    "main_economic_activity_ar",
    "economic_indicator_name_ar",
    "economic_indicator_category_ar",
    "value_qr_000"
FROM "qatar-planning-and-statistics-authority-estimates-of-value-added-by-main-economic-activity-transport-and-communication-statistics-10"
