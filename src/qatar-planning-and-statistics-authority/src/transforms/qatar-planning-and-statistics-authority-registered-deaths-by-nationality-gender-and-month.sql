-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lshhr",
    "month",
    "ljnsy",
    "nationality",
    "lnw",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-registered-deaths-by-nationality-gender-and-month"
