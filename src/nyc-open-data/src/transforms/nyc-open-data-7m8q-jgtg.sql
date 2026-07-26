-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "_month" AS month,
    "_year" AS year,
    "rate"
FROM "nyc-open-data-7m8q-jgtg"
