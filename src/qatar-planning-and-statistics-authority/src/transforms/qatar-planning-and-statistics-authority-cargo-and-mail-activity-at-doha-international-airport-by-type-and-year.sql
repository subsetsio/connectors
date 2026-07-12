-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type",
    "type_ar",
    "total_tons"
FROM "qatar-planning-and-statistics-authority-cargo-and-mail-activity-at-doha-international-airport-by-type-and-year"
