SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-de45c29d-1abf-4357-b1ef-5fa87f5e2e73"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
