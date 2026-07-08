SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-national-diabetes-inpatient-audit-nadia-2018"
WHERE value IS NOT NULL
