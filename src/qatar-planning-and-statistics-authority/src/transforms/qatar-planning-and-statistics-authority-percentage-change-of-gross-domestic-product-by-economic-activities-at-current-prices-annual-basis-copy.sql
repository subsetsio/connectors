-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity",
    "isic_rev_4",
    "isic4_ar",
    "economic_activity_ar",
    "q1",
    "q2",
    "q3",
    "q4"
FROM "qatar-planning-and-statistics-authority-percentage-change-of-gross-domestic-product-by-economic-activities-at-current-prices-annual-basis-copy"
