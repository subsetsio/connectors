-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "educational_status",
    "lhl_lt_lymy",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "age_group",
    "number"
FROM "qatar-planning-and-statistics-authority-employee-working-trainees-at-private-training-centers-by-educational-status-nationality-gender-and"
