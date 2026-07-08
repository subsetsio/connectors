SELECT
    indicator_code,
    indicator_name,
    country_code,
    country_name,
    year,
    value
FROM "world-bank-values"
WHERE value IS NOT NULL
  AND indicator_code IS NOT NULL
  AND country_code IS NOT NULL
  AND year IS NOT NULL
