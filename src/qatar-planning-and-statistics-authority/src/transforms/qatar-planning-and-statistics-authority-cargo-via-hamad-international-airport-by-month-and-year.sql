-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "type",
    "lnw",
    "total_1000_ton"
FROM "qatar-planning-and-statistics-authority-cargo-via-hamad-international-airport-by-month-and-year"
