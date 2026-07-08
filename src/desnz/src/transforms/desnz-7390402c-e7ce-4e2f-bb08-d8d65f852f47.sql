SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-7390402c-e7ce-4e2f-bb08-d8d65f852f47"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
