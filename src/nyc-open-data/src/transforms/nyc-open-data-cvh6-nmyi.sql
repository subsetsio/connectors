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
    "_20122013_overall_grade" AS 20122013_overall_grade,
    "_20122013_overall_score" AS 20122013_overall_score,
    "_201213_overall_percentile" AS 201213_overall_percentile,
    "_20122013_progress_category_score" AS 20122013_progress_category_score,
    "_20122013_progress_grade" AS 20122013_progress_grade,
    "_20122013_performance_category_score" AS 20122013_performance_category_score,
    "_20122013performance_grade" AS 20122013performance_grade,
    "_20122013_environment_category_score" AS 20122013_environment_category_score,
    "_20122013_environment_grade" AS 20122013_environment_grade,
    "_20122013_college_and_career_readiness_score" AS 20122013_college_and_career_readiness_score,
    "_20122013_college_and_career_readiness_grade" AS 20122013_college_and_career_readiness_grade,
    "_20122013_additional_credit" AS 20122013_additional_credit,
    "_201112_progress_report_grade" AS 201112_progress_report_grade,
    "_201011_progress_report_grade" AS 201011_progress_report_grade,
    "_200910_progress_report_grade" AS 200910_progress_report_grade
FROM "nyc-open-data-cvh6-nmyi"
