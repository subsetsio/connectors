SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-065d267f-23bc-4d0e-9a56-52d388d5835c"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
