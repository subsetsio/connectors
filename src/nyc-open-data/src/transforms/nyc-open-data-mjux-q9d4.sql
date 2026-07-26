-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "district",
    "school",
    "principal",
    "progress_report_type",
    "school_level",
    "peer_index",
    "_20112012_overall_grade" AS 20112012_overall_grade,
    "_20112012_overall_score" AS 20112012_overall_score,
    "_201112_overall_percentile" AS 201112_overall_percentile,
    "_20112012_progress_category_score" AS 20112012_progress_category_score,
    "_20112012_progress_grade" AS 20112012_progress_grade,
    "_20112012_performance_category_score" AS 20112012_performance_category_score,
    "_20112012_performance_grade" AS 20112012_performance_grade,
    "_20112012_environment_category_score" AS 20112012_environment_category_score,
    "_20112012_environment_grade" AS 20112012_environment_grade,
    "_20112012_college_and_career_readiness_score" AS 20112012_college_and_career_readiness_score,
    "_20112012_college_and_career_readiness_grade" AS 20112012_college_and_career_readiness_grade,
    "_20112012_additional_credit" AS 20112012_additional_credit,
    "_201011_progress_report_grade" AS 201011_progress_report_grade,
    "_200910_progress_report_grade" AS 200910_progress_report_grade
FROM "nyc-open-data-mjux-q9d4"
