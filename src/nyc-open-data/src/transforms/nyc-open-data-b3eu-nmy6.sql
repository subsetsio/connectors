-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_type",
    "_year" AS year,
    "interval",
    "metric",
    "_value" AS value
FROM "nyc-open-data-b3eu-nmy6"
