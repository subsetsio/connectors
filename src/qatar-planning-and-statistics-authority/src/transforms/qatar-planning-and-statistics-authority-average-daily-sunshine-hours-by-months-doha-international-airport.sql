-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lshhr",
    "month",
    "value_hr"
FROM "qatar-planning-and-statistics-authority-average-daily-sunshine-hours-by-months-doha-international-airport"
