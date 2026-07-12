-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "type",
    "nw",
    "total"
FROM "qatar-planning-and-statistics-authority-arrival-and-departures-via-hamad-international-airport-by-month-and-year"
