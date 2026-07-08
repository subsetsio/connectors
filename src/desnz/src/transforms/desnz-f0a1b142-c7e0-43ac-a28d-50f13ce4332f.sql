SELECT
    resource,
    sheet,
    row_label,
    series,
    value_text,
    TRY_CAST(value_num AS DOUBLE) AS value_num
FROM "desnz-f0a1b142-c7e0-43ac-a28d-50f13ce4332f"
WHERE value_text IS NOT NULL
  AND length(value_text) > 0
