SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-ed44b45d-6651-4767-9f73-92abd3f51e48"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
