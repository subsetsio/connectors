SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-6e7e309e-d2b5-400d-92b7-dd520712aee7"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
