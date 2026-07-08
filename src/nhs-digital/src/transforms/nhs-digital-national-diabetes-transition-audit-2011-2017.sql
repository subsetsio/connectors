SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-national-diabetes-transition-audit-2011-2017"
WHERE value IS NOT NULL
