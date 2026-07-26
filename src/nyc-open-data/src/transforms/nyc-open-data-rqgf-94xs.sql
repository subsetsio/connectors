-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "_source" AS source,
    "question",
    "prevalence",
    "lower_95_confidence_interval",
    "upper_95_confidence_interval"
FROM "nyc-open-data-rqgf-94xs"
