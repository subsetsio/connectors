-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "quarter",
    "rb",
    "indicator",
    "lmw_shr",
    "unit",
    "lwhd",
    "value"
FROM "qatar-planning-and-statistics-authority-quarterly-main-macro-economic-indicators-2022-2023"
