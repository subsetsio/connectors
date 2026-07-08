SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-d24e5973-dc24-4016-b9bd-da9409752498"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
