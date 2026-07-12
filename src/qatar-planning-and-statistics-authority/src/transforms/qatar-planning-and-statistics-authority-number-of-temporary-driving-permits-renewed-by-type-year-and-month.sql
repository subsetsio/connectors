-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "permit_type",
    "nw_ltsryh",
    "total"
FROM "qatar-planning-and-statistics-authority-number-of-temporary-driving-permits-renewed-by-type-year-and-month"
