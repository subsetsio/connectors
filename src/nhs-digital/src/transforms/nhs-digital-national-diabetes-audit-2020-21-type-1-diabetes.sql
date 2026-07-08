SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-national-diabetes-audit-2020-21-type-1-diabetes"
WHERE value IS NOT NULL
