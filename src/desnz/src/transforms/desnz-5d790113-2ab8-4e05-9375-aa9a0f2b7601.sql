SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-5d790113-2ab8-4e05-9375-aa9a0f2b7601"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
