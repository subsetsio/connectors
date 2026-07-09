SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-b2f104db-9670-4076-8c4e-c6b39ef34193"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
