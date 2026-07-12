-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cohort",
    "non_qatari",
    "qatari",
    "total"
FROM "qatar-planning-and-statistics-authority-number-of-students-by-nationality"
