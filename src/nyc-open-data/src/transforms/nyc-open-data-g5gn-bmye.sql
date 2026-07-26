-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "raceethnicity",
    "education",
    "borough",
    "nativity",
    "age",
    "insurance",
    "trimester",
    "diabetes",
    "hypertension",
    "heart_disease",
    "employed",
    "miscarriage",
    "parity",
    "smm",
    "smm_rate"
FROM "nyc-open-data-g5gn-bmye"
