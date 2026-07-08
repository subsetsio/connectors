SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-8f8e436d-816a-4c14-a4de-ad1e73774ec7"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
