-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "school",
    "jae_cluster",
    "jae_course_code",
    "course_name",
    "planned_intake_numbers"
FROM "sg-data-d-45518670214498e31330c6f79e3dbbeb"
