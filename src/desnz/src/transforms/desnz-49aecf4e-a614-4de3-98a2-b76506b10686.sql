SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-49aecf4e-a614-4de3-98a2-b76506b10686"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
