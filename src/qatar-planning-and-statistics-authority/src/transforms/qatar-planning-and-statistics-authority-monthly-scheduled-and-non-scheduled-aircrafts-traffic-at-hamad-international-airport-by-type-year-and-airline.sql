-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "airline",
    "shrk_tyrn",
    "type",
    "lnw",
    "total"
FROM "qatar-planning-and-statistics-authority-monthly-scheduled-and-non-scheduled-aircrafts-traffic-at-hamad-international-airport-by-type-year-and-airline"
