SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-55efc916-edbb-4468-8c71-0786cb9463c1"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
