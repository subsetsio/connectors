-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity",
    "lnsht_lqtsdy",
    "educational_status",
    "lhl_lt_lymy",
    "value"
FROM "qatar-planning-and-statistics-authority-economically-active-females-15-years-and-above-by-educational-status-and-economic-activity"
