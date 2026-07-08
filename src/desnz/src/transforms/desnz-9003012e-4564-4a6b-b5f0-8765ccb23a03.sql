SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-9003012e-4564-4a6b-b5f0-8765ccb23a03"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
