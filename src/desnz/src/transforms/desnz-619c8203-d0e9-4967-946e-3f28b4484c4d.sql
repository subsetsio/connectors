SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-619c8203-d0e9-4967-946e-3f28b4484c4d"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
