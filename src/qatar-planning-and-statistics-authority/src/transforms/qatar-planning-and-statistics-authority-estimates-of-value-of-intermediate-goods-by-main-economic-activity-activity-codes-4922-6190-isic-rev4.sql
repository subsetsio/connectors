-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "intermediate_goods",
    "main_economic_activity_ar",
    "intermediate_goods_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-estimates-of-value-of-intermediate-goods-by-main-economic-activity-activity-codes-4922-6190-isic-rev4"
