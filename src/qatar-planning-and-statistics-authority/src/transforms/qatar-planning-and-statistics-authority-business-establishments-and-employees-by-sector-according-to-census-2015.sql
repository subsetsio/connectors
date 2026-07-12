-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "lqt",
    "employees_number_dd_lmshtglwn",
    "establishments_number_dd_lmnshat",
    "employees_lmshtglwn",
    "establishments_lmnshat"
FROM "qatar-planning-and-statistics-authority-business-establishments-and-employees-by-sector-according-to-census-2015"
