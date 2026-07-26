-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "sheet_name",
    "row_number",
    "Teacher Loan Forgiveness Program" AS teacher_loan_forgiveness_program,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Automatic Closed School Discharge (ACSD) Report" AS automatic_closed_school_discharge_acsd_report,
    "Unnamed: 5" AS unnamed_5,
    "Automatic Closed School Discharges (ACSD) Processed by School" AS automatic_closed_school_discharges_acsd_processed_by_school,
    "Unnamed: 6" AS unnamed_6
FROM "u-s-department-of-education-loan-forgiveness-reports"
