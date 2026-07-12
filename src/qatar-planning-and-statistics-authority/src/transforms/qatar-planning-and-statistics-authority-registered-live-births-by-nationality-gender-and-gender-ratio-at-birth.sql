-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ljnsy",
    "nationality",
    "lnw",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-nationality-gender-and-gender-ratio-at-birth"
