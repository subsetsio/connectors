-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "admin_district",
    "geographical_district",
    "location_code",
    "dbn",
    "school_level",
    "student_enrollment",
    "full_time_licensed_pe_teachers",
    "f_status_pe_teachers",
    "itinerant_pe_teachers",
    "sum_of_f_status_and_itinerant",
    "total_part_time_and_full_time_pe_teachers",
    "shared_pe_teachers_with_another_school",
    "ratio_of_full_time_licensed_pe_teachers_to_students"
FROM "nyc-open-data-ajin-fesn"
