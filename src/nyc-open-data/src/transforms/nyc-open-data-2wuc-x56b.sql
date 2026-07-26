-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_type",
    "_year" AS year,
    "_month" AS month,
    "metric",
    "count",
    "rate_per_100_adp"
FROM "nyc-open-data-2wuc-x56b"
