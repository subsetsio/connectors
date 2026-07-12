-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "type_of_values",
    "revenue_types",
    "value_added_lqym_lmdf_qr_000",
    "main_economic_activity_ar",
    "type_of_values_ar",
    "revenue_types_ar"
FROM "qatar-planning-and-statistics-authority-estimates-of-value-added-by-main-economic-activity-10-employees-and-more-activity-codes-60-64-isic"
