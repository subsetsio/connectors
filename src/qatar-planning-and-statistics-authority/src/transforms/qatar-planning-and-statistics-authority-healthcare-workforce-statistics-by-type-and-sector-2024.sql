-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "category",
    "sector",
    "number",
    "rate_per_1_000_population",
    "population_per_professional"
FROM "qatar-planning-and-statistics-authority-healthcare-workforce-statistics-by-type-and-sector-2024"
