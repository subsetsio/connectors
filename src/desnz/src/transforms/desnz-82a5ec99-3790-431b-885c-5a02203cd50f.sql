SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-82a5ec99-3790-431b-885c-5a02203cd50f"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
