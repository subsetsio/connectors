-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "_location" AS location,
    "location_type",
    "total_guidance_counselor_gc_social_worker_sw",
    "total_gc",
    "atr_total_gc_sw",
    "atr_total_gc",
    "full_time_gc",
    "part_time_gc",
    "bilingual_gc",
    "serving_more_than_one_location",
    "notes",
    "single_shepherd",
    "learning_to_work_program",
    "community_school_cbo_partner",
    "_201718_sy_enrollment" AS 201718_sy_enrollment,
    "ratio_gc_sw",
    "ratio_gc_only"
FROM "nyc-open-data-khci-nhn2"
