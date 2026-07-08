SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-eb8e6778-85de-47f8-ae5d-204bc5b4f2cd"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
