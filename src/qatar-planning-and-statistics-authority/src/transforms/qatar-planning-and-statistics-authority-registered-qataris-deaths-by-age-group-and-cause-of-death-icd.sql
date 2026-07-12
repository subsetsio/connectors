-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "ljns",
    "age_group",
    "lfy_l_mry",
    "cause_of_death",
    "sbb_lwf",
    "total"
FROM "qatar-planning-and-statistics-authority-registered-qataris-deaths-by-age-group-and-cause-of-death-icd"
