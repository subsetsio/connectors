-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_type",
    "borough",
    "district",
    "dbn",
    "school_name",
    "grade",
    "_year" AS year,
    "demographic_category",
    "demographic_variable",
    "total_days",
    "days_absent",
    "days_present",
    "attendance",
    "contributing_20_total_days",
    "chronically_absent",
    "chronically_absent_1"
FROM "nyc-open-data-mg8s-7r2b"
