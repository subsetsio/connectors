-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_group",
    "training_agency",
    "jh_ltdryb",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-trainees-at-training-centers-by-training-agency-gender-and-age-group0"
