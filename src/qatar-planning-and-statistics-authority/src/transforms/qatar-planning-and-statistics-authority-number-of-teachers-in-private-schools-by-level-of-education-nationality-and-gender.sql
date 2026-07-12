-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "lmrhl_lt_lymy",
    "nationality",
    "ljnsy",
    "gender",
    "lnw",
    "number"
FROM "qatar-planning-and-statistics-authority-number-of-teachers-in-private-schools-by-level-of-education-nationality-and-gender"
