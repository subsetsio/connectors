SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-21db6396-3daf-4d90-8b3f-054995256018"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
