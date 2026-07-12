-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "area",
    "lmntq",
    "domain0",
    "lntq",
    "unit",
    "value"
FROM "qatar-planning-and-statistics-authority-natural-protected-areas-in-qatar-land-and-marine"
