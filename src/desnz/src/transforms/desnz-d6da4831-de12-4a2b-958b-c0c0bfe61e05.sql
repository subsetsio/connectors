SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-d6da4831-de12-4a2b-958b-c0c0bfe61e05"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
