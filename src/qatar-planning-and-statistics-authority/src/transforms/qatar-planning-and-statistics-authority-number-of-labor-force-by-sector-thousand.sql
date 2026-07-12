-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sector",
    "lqt",
    "2022_000",
    "2023_000",
    "annual_growth_rate"
FROM "qatar-planning-and-statistics-authority-number-of-labor-force-by-sector-thousand"
