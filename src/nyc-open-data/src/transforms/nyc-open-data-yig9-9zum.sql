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
    "_20102011_overall_grade" AS 20102011_overall_grade,
    "_20102011_overall_score" AS 20102011_overall_score,
    "_20102011_environment_category_score" AS 20102011_environment_category_score,
    "_20102011_environment_grade" AS 20102011_environment_grade,
    "_20102011_performance_category_score" AS 20102011_performance_category_score,
    "_20102011_performance_grade" AS 20102011_performance_grade,
    "_20102011_progress_category_score" AS 20102011_progress_category_score,
    "_20102011_progress_grade" AS 20102011_progress_grade,
    "_20102011_additional_credit" AS 20102011_additional_credit,
    "_200910_progress_report_grade" AS 200910_progress_report_grade
FROM "nyc-open-data-yig9-9zum"
