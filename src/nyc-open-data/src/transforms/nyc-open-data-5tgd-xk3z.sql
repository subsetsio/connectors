-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "disease",
    "gender",
    "borough",
    "age_category",
    "case_counts"
FROM "nyc-open-data-5tgd-xk3z"
