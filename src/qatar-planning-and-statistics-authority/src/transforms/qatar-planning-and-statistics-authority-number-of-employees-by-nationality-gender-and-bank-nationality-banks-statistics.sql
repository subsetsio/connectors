-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "bank_nationality_ar",
    "bank_nationality",
    "nationality_ar",
    "nationality",
    "gender_ar",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-employees-by-nationality-gender-and-bank-nationality-banks-statistics"
