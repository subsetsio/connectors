SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-4b7b7f64-0b97-4a6e-8e45-1218b9a81876"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
