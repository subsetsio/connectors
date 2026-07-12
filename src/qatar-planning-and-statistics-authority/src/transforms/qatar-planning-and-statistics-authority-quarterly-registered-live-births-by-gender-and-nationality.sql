-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "quarter",
    "nationality",
    "ljnsy",
    "male",
    "female",
    "total"
FROM "qatar-planning-and-statistics-authority-quarterly-registered-live-births-by-gender-and-nationality"
