SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-e7d4c1cf-45a0-4070-878f-24ad9641f655"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
