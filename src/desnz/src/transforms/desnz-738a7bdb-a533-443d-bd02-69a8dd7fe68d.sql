SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-738a7bdb-a533-443d-bd02-69a8dd7fe68d"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
