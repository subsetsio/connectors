SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-473afefd-9028-48d1-a959-c865c1387a9d"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
