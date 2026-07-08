SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-995df3b9-993e-403b-a527-a62ff0b56ca3"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
