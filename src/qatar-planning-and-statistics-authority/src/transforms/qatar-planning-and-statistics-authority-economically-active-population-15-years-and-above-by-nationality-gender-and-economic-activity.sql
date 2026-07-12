-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "gender",
    "lnw",
    "economic_activity",
    "lnsht_lqtsdy",
    "count"
FROM "qatar-planning-and-statistics-authority-economically-active-population-15-years-and-above-by-nationality-gender-and-economic-activity"
