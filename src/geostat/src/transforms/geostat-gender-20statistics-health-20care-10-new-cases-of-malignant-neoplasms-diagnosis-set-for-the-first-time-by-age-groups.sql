-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("year" AS BIGINT) AS year,
    "age",
    "value"
FROM "geostat-gender-20statistics-health-20care-10-new-cases-of-malignant-neoplasms-diagnosis-set-for-the-first-time-by-age-groups"
