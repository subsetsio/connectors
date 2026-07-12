-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_year",
    "females",
    "males",
    "total"
FROM "qatar-planning-and-statistics-authority-population-estimates-by-gender-as-of-mid-year-1986-2023"
