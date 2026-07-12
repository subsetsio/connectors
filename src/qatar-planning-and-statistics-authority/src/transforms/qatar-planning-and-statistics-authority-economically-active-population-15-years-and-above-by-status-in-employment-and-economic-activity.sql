-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity",
    "lnsht_lqtsdy",
    "occupation_status",
    "lhl_l_mly",
    "number"
FROM "qatar-planning-and-statistics-authority-economically-active-population-15-years-and-above-by-status-in-employment-and-economic-activity"
