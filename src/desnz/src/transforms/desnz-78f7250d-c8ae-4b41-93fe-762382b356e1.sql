SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-78f7250d-c8ae-4b41-93fe-762382b356e1"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
