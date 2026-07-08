SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-1656fb7d-1ca3-462d-a11b-8078acc33275"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
