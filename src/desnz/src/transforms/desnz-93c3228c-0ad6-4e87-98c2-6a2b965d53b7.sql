SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-93c3228c-0ad6-4e87-98c2-6a2b965d53b7"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
