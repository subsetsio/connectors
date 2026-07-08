SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-fdb6be5f-59bb-4722-b72d-6e4dbc0f0626"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
