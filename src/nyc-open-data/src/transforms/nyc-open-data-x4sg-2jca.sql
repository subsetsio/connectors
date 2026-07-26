-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "admin_district",
    "geographical_district",
    "pe_works_cohort",
    "dbn",
    "school_level",
    "student_enrollment",
    "full_time_licensed_pe_teachers",
    "part_time_licensed_pe_teachers_f_status_pe_teachers_as_of_10312015_ape_teachers_not_included_elementary_early_childhood_and_k8_teachers_providing_physical_education_under_a_common_branch_license_are_not_included",
    "part_time_licensed_pe_teachers_itinerant_pe_teachers_as_of_10312015_ape_teachers_not_included_elementary_early_childhood_and_k8_teachers_providing_physical_education_under_a_common_branch_license_are_not_included",
    "part_time_licensed_pe_teachers_sum_of_f_status_and_itinerant",
    "total_part_time_and_full_time_licensed_pe_teachers_as_of_10312015_ape_teachers_not_included_elementary_early_childhood_and_k8_teachers_providing_physical_education_under_a_common_branch_license_are_not_included",
    "shared_licensed_pe_teachers_with_another_school_as_of_10312015_ape_teachers_not_included_elementary_early_childhood_and_k8_teachers_providing_physical_education_under_a_common_branch_license_are_not_included",
    "ratio_of_full_time_licensed_pe_teachers_to_students_as_of_10312015_ape_teachers_not_included_elementary_early_childhood_and_k8_teachers_providing_physical_education_under_a_common_branch_license_are_not_included"
FROM "nyc-open-data-x4sg-2jca"
