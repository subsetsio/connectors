-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "ljns",
    "economic_activity",
    "lnsht_lqtsdy",
    "total"
FROM "qatar-planning-and-statistics-authority-percentage-of-active-population-15-years-and-above-by-economic-activity-and-gender"
