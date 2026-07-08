SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-national-audit-of-pulmonary-hypertension-13th-annual-report-2021-22"
WHERE value IS NOT NULL
