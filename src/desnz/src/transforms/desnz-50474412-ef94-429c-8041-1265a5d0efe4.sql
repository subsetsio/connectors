SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-50474412-ef94-429c-8041-1265a5d0efe4"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
