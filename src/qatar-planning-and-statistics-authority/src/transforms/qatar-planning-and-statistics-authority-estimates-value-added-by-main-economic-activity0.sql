-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "lnsht_ltfsyly",
    "detailed_activity",
    "lmw_shr_lqtsdy",
    "economic_indicator",
    "mkwn_lmw_shr",
    "indicator_component",
    "code",
    "value_qr"
FROM "qatar-planning-and-statistics-authority-estimates-value-added-by-main-economic-activity0"
