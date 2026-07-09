SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-2673218b-0888-4617-a94e-9df90f75117f"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
