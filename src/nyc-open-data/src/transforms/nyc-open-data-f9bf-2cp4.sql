-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "num_of_sat_test_takers",
    "sat_critical_reading_avg_score",
    "sat_math_avg_score",
    "sat_writing_avg_score"
FROM "nyc-open-data-f9bf-2cp4"
