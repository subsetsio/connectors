SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-df7e7e32-7c31-4970-a1c4-900a8c2111e8"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
