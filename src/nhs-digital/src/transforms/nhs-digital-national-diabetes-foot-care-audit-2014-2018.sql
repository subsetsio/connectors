SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-national-diabetes-foot-care-audit-2014-2018"
WHERE value IS NOT NULL
