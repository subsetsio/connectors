SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-c647e722-b691-47e9-a765-a22e24f05a04"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
