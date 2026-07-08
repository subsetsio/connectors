SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-acd6dbb9-1958-4605-8a49-8b15f5022a7b"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
