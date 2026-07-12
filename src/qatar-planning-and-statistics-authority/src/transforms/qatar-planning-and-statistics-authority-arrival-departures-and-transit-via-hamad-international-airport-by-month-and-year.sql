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
    "total"
FROM "qatar-planning-and-statistics-authority-arrival-departures-and-transit-via-hamad-international-airport-by-month-and-year"
