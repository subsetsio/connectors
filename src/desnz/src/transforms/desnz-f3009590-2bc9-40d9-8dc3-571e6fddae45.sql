SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-f3009590-2bc9-40d9-8dc3-571e6fddae45"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
