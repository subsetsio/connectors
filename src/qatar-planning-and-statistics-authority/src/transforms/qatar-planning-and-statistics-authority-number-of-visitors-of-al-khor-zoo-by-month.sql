-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sn",
    "month_ar",
    "month",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-visitors-of-al-khor-zoo-by-month"
