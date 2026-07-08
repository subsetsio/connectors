SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-a77294d6-b676-4f95-b584-ceabc65f36bd"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
