-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "location_type",
    "total_guidance_counselors_gc_social_workers_sw_includes_gcs_sws_atrs_school_response_clinicians_high_needs_counselors_high_need_sws_single_shepherds_bridging_the_gap_sws",
    "total_gc",
    "total_sw",
    "fulltime_gc",
    "fulltime_sw",
    "parttime_gc",
    "parttime_sw",
    "bilingual_gc",
    "bilingual_sw",
    "gc_serving_more_than_one_location",
    "sw_serving_more_than_one_location",
    "high_needs_gc",
    "high_needs_sw",
    "bridging_the_gap",
    "school_response_clinician",
    "single_shepherd",
    "learning_to_work",
    "school_psychologist_providing_mandated_counseling",
    "cbo_partner_for_mental_health_support",
    "_202021_sy_enrollment" AS 202021_sy_enrollment,
    "ratio_gc_sw",
    "ratio_gc_only",
    "ratio_sw_only"
FROM "nyc-open-data-vmdx-uykr"
