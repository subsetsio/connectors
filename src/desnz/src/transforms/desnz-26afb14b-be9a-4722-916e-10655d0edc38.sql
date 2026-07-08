SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-26afb14b-be9a-4722-916e-10655d0edc38"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
