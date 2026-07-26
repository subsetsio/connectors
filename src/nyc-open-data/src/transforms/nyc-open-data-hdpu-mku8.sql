-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "total_parent_response_rate",
    "total_teacher_response_rate",
    "total_student_response_rate"
FROM "nyc-open-data-hdpu-mku8"
