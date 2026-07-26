-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grade",
    "category",
    "_year" AS year,
    "total_days",
    "days_absent",
    "days_present",
    "attendance",
    "contributing_10_total_days_and_1_pres_day",
    "chronically_absent",
    "chronically_absent_1"
FROM "nyc-open-data-sgsi-66kk"
