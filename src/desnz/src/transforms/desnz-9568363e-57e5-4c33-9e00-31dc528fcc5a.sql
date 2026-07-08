SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-9568363e-57e5-4c33-9e00-31dc528fcc5a"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
