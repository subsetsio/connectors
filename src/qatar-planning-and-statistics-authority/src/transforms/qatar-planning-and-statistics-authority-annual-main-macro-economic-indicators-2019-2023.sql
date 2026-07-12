-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "lmw_shr",
    "unit",
    "lwhd",
    "annee",
    "value"
FROM "qatar-planning-and-statistics-authority-annual-main-macro-economic-indicators-2019-2023"
