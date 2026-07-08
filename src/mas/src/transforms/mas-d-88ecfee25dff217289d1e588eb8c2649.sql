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
FROM "mas-d-88ecfee25dff217289d1e588eb8c2649"
WHERE data_series IS NOT NULL
  AND TRY_CAST(REPLACE(TRIM(value_raw), ',', '') AS DOUBLE) IS NOT NULL
