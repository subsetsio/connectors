SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-28d823ff-310b-4620-8ba2-58dbd1d0c7c5"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
