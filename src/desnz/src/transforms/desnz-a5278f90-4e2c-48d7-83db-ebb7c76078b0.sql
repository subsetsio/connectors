SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-a5278f90-4e2c-48d7-83db-ebb7c76078b0"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
