SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-general-pharmaceutical-services"
WHERE value IS NOT NULL
