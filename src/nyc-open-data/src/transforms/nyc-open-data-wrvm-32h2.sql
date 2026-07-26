-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "boro",
    "csd",
    "city_council_district",
    "bldg_id",
    "bldg_name",
    "of_student_bathrooms",
    "are_bathrooms_opened_all_the_time",
    "is_any_bathroom_shared",
    "of_noninstructional_space_used",
    "is_any_noninstructional_space_shared"
FROM "nyc-open-data-wrvm-32h2"
