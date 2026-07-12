-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "disease",
    "lmrd",
    "gender",
    "lnw",
    "number_of_reported_cases_dd_lhlt_lmsjl"
FROM "qatar-planning-and-statistics-authority-number-of-reported-infectious-disease-cases-by-disease-and-gender"
