SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-national-diabetes-inpatient-safety-audit-ndisa-2018-2021"
WHERE value IS NOT NULL
