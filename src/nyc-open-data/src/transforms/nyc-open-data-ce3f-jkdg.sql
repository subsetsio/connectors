-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "average_score_regents_integrated_algebra",
    "_passing" AS passing,
    "at_college_ready_threshold",
    "average_score_regents_english",
    "passing_1",
    "at_college_ready_threshold_1",
    "average_score_regents_us_history",
    "passing_2",
    "average_score_regents_global_history",
    "passing_3",
    "average_score_regents_earth_science",
    "passing_4",
    "average_score_regents_living_environment",
    "passing_5",
    "average_score_regents_languages_other_than_english",
    "passing_6",
    "average_score_sat_math",
    "average_score_sat_critical_reading",
    "average_score_sat_writing",
    "postsecondary_enrollment_rate_6_months",
    "_2_year_or_4_year_college_6_months" AS 2_year_or_4_year_college_6_months,
    "cuny_6_months",
    "nys_public_6_months",
    "nys_private_6_months",
    "out_of_state_6_months",
    "public_service_6_months",
    "vocational_program_6_months",
    "cri_of_6_year_cohort",
    "attaining_regents_diplma_6_year",
    "attaining_math_college_readiness_standard",
    "attaining_english_college_readiness_standard"
FROM "nyc-open-data-ce3f-jkdg"
