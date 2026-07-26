-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "survey",
    "_year" AS year,
    "denominator",
    "question",
    "prevalence",
    "lower_95_ci",
    "upper_95_ci"
FROM "nyc-open-data-wi3r-8uzb"
