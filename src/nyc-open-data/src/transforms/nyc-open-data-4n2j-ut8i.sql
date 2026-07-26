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
    "_20092010_overall_grade" AS 20092010_overall_grade,
    "_20092010_overall_score" AS 20092010_overall_score,
    "_20092010_environment_category_score" AS 20092010_environment_category_score,
    "_20092010_environment_grade" AS 20092010_environment_grade,
    "_20092010_performance_category_score" AS 20092010_performance_category_score,
    "_20092010_performance_grade" AS 20092010_performance_grade,
    "_20092010_progress_category_score" AS 20092010_progress_category_score,
    "_20092010_progress_grade" AS 20092010_progress_grade,
    "_20092010_additional_credit" AS 20092010_additional_credit,
    "_200809_progress_report_grade" AS 200809_progress_report_grade
FROM "nyc-open-data-4n2j-ut8i"
