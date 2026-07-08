SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-44dea418-483e-43f1-80f8-4694b2edaa01"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
