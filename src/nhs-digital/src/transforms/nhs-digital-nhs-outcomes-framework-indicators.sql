SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-nhs-outcomes-framework-indicators"
WHERE value IS NOT NULL
