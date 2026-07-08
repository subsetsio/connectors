SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-86a4555e-6f38-4529-8647-542cc6223162"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
