-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "bank_nationality_ar",
    "bank_nationality",
    "indicator_ar",
    "indicator",
    "nationality_ar",
    "nationality",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-employees-and-estimated-compensation-by-nationality-and-bank-nationality-banks-statistics"
