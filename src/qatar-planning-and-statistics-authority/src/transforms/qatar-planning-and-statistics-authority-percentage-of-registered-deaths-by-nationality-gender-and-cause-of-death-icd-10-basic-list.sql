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
    "sbb_lwf",
    "percentage"
FROM "qatar-planning-and-statistics-authority-percentage-of-registered-deaths-by-nationality-gender-and-cause-of-death-icd-10-basic-list"
