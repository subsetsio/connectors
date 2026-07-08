SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-ed629618-7b69-465d-8e0a-0546b1809fc7"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
