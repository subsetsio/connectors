SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-5370c0bb-d3bb-4a45-829a-1437018fe13d"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
