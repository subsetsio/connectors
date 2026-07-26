-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "district",
    "school",
    "school_support_organizationnetwork",
    "progress_report_type",
    "school_level",
    "peer_index",
    "grade",
    "overall_score",
    "environment_category_score",
    "performance_category_score",
    "progress_category_score",
    "additional_credit",
    "quality_review_score"
FROM "nyc-open-data-fzv4-jan3"
