SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-cf609fce-0158-4b3d-901a-b81951f4eeeb"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
