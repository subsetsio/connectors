SELECT DISTINCT
    report_number,
    freq_type,
    mask AS period,
    indicator,
    col_label,
    TRY_CAST(replace(replace(value, ',', ''), ' ', '') AS DOUBLE) AS value
FROM "beijing-municipal-bureau-of-statistics-01-ls-2-01-2"
WHERE value IS NOT NULL
  AND trim(value) <> ''
  AND TRY_CAST(replace(replace(value, ',', ''), ' ', '') AS DOUBLE) IS NOT NULL
