-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "number_of_test_takers",
    "critical_reading_mean",
    "mathematics_mean",
    "writing_mean"
FROM "nyc-open-data-zt9s-n5aj"
