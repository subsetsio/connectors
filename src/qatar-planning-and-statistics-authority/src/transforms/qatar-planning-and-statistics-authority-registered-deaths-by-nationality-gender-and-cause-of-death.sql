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
    "cause_of_death",
    "sbb_lwfh",
    "total"
FROM "qatar-planning-and-statistics-authority-registered-deaths-by-nationality-gender-and-cause-of-death"
