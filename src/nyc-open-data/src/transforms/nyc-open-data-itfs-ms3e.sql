-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "schoolname",
    "ap_test_takers",
    "total_exams_taken",
    "number_of_exams_with_scores_3_4_or_5"
FROM "nyc-open-data-itfs-ms3e"
