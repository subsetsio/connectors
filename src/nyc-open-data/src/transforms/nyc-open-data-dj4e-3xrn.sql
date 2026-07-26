-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "district",
    "school",
    "principal",
    "_200708_school_support_organization" AS 200708_school_support_organization,
    "progress_report_type",
    "school_level",
    "peer_index",
    "overall_grade",
    "overall_score",
    "environment_category_score",
    "environment_grade",
    "performance_category_score",
    "performance_grade",
    "progress_category_score",
    "progress_grade",
    "additional_credit",
    "_200607_progress_report_grade" AS 200607_progress_report_grade,
    "_200708_quality_review_score" AS 200708_quality_review_score,
    "_200607_federal_accountability_status" AS 200607_federal_accountability_status
FROM "nyc-open-data-dj4e-3xrn"
