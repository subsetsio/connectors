SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-national-audit-of-pulmonary-hypertension-12th-annual-report-2020-21"
WHERE value IS NOT NULL
