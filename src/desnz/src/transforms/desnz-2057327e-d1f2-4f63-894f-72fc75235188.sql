SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-2057327e-d1f2-4f63-894f-72fc75235188"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
