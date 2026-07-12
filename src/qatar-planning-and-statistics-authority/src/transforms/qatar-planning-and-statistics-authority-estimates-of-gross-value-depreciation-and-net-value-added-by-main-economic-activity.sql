-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "lnsht_lqtsd_lry_ysy",
    "net_value_added",
    "depreciations",
    "gross_value_added"
FROM "qatar-planning-and-statistics-authority-estimates-of-gross-value-depreciation-and-net-value-added-by-main-economic-activity"
