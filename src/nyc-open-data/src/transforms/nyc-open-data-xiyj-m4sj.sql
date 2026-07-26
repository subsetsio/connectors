-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "school_type",
    "parent_response_rate",
    "teacher_response_rate",
    "student_response_rate",
    "total_safety_and_respect_score",
    "total_communication_score",
    "total_engagement_score",
    "total_academic_expectations_score"
FROM "nyc-open-data-xiyj-m4sj"
