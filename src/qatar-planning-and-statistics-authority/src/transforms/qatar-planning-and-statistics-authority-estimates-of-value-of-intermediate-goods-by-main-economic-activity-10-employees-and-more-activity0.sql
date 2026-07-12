-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "intermediate_goods",
    "estimate_of_value_tqdyrt_qym_qr_000",
    "lnsht_lqtsdy_lry_ysy",
    "lmsltzmt_lsl_y"
FROM "qatar-planning-and-statistics-authority-estimates-of-value-of-intermediate-goods-by-main-economic-activity-10-employees-and-more-activity0"
