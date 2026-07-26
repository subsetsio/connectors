-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "total_test",
    "positive_test",
    "percent_positive",
    "percent_positive_7days_agg",
    "uptdate"
FROM "nyc-open-data-7434-7ua6"
