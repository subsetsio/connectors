SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-national-diabetes-audit-report-1-care-processes-and-treatment-targets-2017-18-full-report"
WHERE value IS NOT NULL
