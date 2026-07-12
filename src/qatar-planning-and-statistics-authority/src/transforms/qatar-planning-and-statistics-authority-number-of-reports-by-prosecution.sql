-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "prosecution",
    "number_of_reports",
    "prosecution_ar"
FROM "qatar-planning-and-statistics-authority-number-of-reports-by-prosecution"
