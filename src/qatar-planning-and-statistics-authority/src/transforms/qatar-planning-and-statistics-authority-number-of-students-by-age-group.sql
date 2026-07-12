-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cohort",
    "under_24_years",
    "24_29_years",
    "30_34_years",
    "35_39_years",
    "40_years_and_above",
    "total"
FROM "qatar-planning-and-statistics-authority-number-of-students-by-age-group"
