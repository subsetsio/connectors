SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-1715ab16-2a5a-49ac-8aef-0b9d0cf741b2"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
