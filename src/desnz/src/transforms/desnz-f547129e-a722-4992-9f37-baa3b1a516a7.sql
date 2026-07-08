SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-f547129e-a722-4992-9f37-baa3b1a516a7"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
