SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-9cba4b9b-18bb-4d03-b77c-117315d1e1ea"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
