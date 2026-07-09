SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-1a7347c5-8758-427b-825b-31e0ff417784"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
