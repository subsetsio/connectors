-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "economic_activity",
    "lnsht_lqtsdy",
    "2023_q2",
    "2024_q1",
    "2024_q2",
    "change_q2_24_q1_24",
    "change_q2_24_q2_23"
FROM "qatar-planning-and-statistics-authority-estimates-of-quarterly-gross-domestic-product-by-economic-activities-at-current-prices-q2-2024"
