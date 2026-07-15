-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "jae_cluster",
    "jae_course_code",
    "course_name",
    "gceo_cut_off_point"
FROM "sg-data-d-eb7bb85a49e021e63f9cb7b54497a400"
