SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-480984d5-13d7-48b1-93c8-2a0871ef5543"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
