SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-9a1e58e5-d1b6-457d-a414-335ca546d52c"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
