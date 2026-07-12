-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sport_facilities",
    "sport_facilities_ar",
    "total"
FROM "qatar-planning-and-statistics-authority-sport-facilities-by-type-2022"
