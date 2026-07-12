-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "month_ar",
    "airline",
    "airline_ar",
    "type",
    "type_ar",
    "total"
FROM "qatar-planning-and-statistics-authority-monthly-scheduled-and-non-scheduled-aircrafts-traffic-by-type-year-and-airline"
