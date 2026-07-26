-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_information_school_name",
    "location_type",
    "total_guidance_counselors_gc_social_workers_sw_includes_gcs_sws_atrs_school_response_clinicians_high_needs_counselors_high_need_sws_single_shepherds_bridging_the_gap_sws",
    "total_gc",
    "total_sw",
    "counts_by_role_specificaiton_fulltime_gc",
    "counts_by_role_specification_fulltime_sw",
    "count_by_role_specification_parttime_gc",
    "count_by_role_specification_parttime_sw",
    "additional_role_specifications_bilingual_gc",
    "additional_role_specifications_bilingual_sw",
    "additional_role_specifications_gc_serving_more_than_one_location",
    "additional_role_specifications_sw_serving_more_than_one_location",
    "program_designations_included_in_counts_bridging_the_gap",
    "program_designations_included_in_counts_high_needs_sw",
    "program_designations_included_in_counts_high_needs_gc",
    "program_designations_included_in_counts_school_response_clinician",
    "program_designations_included_in_counts_single_shepherd",
    "additional_supports_learning_to_work",
    "additional_supports_cbo_partner",
    "enrollment_and_ratios_201920_sy_enrollment",
    "enrollment_and_ratios_ratio_gc_sw",
    "enrollment_and_ratios_ratio_gc_only",
    "enrollment_and_ratios_ratio_sw_only"
FROM "nyc-open-data-yphg-6fug"
