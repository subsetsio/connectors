SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-723c243d-2f1a-4d27-8b61-cdb93e5b10ff"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
