SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-b6a31316-c69b-44c6-babd-d0b76448b030"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
