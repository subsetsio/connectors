-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator_name",
    "unit",
    "value"
FROM "qatar-planning-and-statistics-authority-demand-for-water-by-type-number-and-growth-rate-of-subscribers"
