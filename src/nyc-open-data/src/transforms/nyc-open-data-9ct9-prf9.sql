-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "num_of_ap_test_takers",
    "num_of_ap_total_exams_taken",
    "num_of_ap_exams_passed"
FROM "nyc-open-data-9ct9-prf9"
