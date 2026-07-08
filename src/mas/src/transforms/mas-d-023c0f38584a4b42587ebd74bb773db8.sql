SELECT
  trim(data_series) AS data_series,
  CASE
    WHEN regexp_full_match(period_raw, '^\d{4}[A-Z][a-z]{2}$')
      THEN strftime(strptime(period_raw, '%Y%b'), '%Y-%m')
    WHEN regexp_full_match(period_raw, '^\d{4}\dQ$')
      THEN regexp_extract(period_raw, '^(\d{4})(\d)Q$', 1) || '-Q' ||
           regexp_extract(period_raw, '^(\d{4})(\d)Q$', 2)
    WHEN regexp_full_match(period_raw, '^\d{4}$')
      THEN period_raw
    ELSE NULL
  END AS period,
  TRY_CAST(REPLACE(TRIM(value_raw), ',', '') AS DOUBLE) AS value
FROM "mas-d-023c0f38584a4b42587ebd74bb773db8"
WHERE data_series IS NOT NULL
  AND TRY_CAST(REPLACE(TRIM(value_raw), ',', '') AS DOUBLE) IS NOT NULL
