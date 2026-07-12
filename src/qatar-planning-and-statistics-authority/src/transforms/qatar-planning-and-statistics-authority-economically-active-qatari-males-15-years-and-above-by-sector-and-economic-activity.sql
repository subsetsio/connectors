-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity",
    "lnsht_lqtsdy",
    "sector",
    "lqt",
    "number"
FROM "qatar-planning-and-statistics-authority-economically-active-qatari-males-15-years-and-above-by-sector-and-economic-activity"
