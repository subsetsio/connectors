-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_group",
    "nationality",
    "ljnsy",
    "educational_level",
    "lhl_lt_lymy",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-trainees-in-private-training-centers-unemployed-by-educational-level-gender-nationality-and-age"
