-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cohort",
    "faculty_of_economics_management_and_public_policy",
    "faculty_of_social_sciences_and_humanities",
    "total"
FROM "qatar-planning-and-statistics-authority-number-of-enrolled-students-by-college"
