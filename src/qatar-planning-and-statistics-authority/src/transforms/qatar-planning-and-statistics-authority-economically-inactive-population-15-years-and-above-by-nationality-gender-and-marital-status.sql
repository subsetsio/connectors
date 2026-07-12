-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "marital_status",
    "lhl_lzwjy",
    "value"
FROM "qatar-planning-and-statistics-authority-economically-inactive-population-15-years-and-above-by-nationality-gender-and-marital-status"
