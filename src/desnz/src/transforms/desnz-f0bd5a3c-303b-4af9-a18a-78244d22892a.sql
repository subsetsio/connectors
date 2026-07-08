SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-f0bd5a3c-303b-4af9-a18a-78244d22892a"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
