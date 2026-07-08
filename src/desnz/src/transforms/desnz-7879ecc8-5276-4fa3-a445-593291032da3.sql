SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-7879ecc8-5276-4fa3-a445-593291032da3"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
