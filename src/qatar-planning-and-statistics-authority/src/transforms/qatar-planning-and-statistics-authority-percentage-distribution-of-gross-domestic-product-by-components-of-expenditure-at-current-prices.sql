-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lnsht_lqtsdy",
    "q1",
    "q2",
    "q3",
    "q4",
    "economic_activity",
    "code"
FROM "qatar-planning-and-statistics-authority-percentage-distribution-of-gross-domestic-product-by-components-of-expenditure-at-current-prices"
