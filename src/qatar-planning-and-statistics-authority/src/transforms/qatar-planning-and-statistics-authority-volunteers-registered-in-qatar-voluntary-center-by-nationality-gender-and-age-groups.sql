-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_groups",
    "age_groups_ar",
    "qataris_males",
    "qataris_females",
    "non_qataris_males",
    "non_qataris_females"
FROM "qatar-planning-and-statistics-authority-volunteers-registered-in-qatar-voluntary-center-by-nationality-gender-and-age-groups"
