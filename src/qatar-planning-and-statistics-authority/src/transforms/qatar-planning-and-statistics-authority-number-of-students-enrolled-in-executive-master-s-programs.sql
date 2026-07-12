-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cohort",
    "number_of_students"
FROM "qatar-planning-and-statistics-authority-number-of-students-enrolled-in-executive-master-s-programs"
