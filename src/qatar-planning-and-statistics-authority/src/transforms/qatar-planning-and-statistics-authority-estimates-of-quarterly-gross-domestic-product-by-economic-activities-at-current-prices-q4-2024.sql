-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "economic_activity",
    "economic_activity0",
    "2023_q4",
    "2024_q3",
    "2024_q4",
    "change_q4_24_q3_24",
    "change_q4_24_q4_23"
FROM "qatar-planning-and-statistics-authority-estimates-of-quarterly-gross-domestic-product-by-economic-activities-at-current-prices-q4-2024"
