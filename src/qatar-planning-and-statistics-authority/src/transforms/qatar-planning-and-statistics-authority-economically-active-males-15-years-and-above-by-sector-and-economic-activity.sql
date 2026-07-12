-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "lqt",
    "economic_activity",
    "lnsht_lqtsdy",
    "total"
FROM "qatar-planning-and-statistics-authority-economically-active-males-15-years-and-above-by-sector-and-economic-activity"
