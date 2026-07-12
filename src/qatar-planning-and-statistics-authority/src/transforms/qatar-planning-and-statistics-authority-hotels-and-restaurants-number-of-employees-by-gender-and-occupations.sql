-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "gender",
    "occupation",
    "number_of_employees_dd_lmshtglyn",
    "lmhn",
    "lnw"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-number-of-employees-by-gender-and-occupations"
