SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-b264edb9-4a78-4977-a871-c9561a3ef8cc"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
