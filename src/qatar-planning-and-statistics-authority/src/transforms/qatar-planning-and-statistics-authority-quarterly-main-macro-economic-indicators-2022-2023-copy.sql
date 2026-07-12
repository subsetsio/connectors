-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "lmw_shr",
    "unit",
    "lwhd",
    strptime("date", '%Y-%m')::DATE AS date,
    "value"
FROM "qatar-planning-and-statistics-authority-quarterly-main-macro-economic-indicators-2022-2023-copy"
