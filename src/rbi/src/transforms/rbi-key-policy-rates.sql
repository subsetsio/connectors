-- Keep only the %-denominated monetary/policy rates; exclude the
-- mixed-unit ticker rows (Exchange Rate in INR/USD, CPI Inflation)
-- that share the homepage snapshot but are not policy rates.
SELECT
    name AS rate_name,
    CAST(rate AS DOUBLE) AS rate_percent,
    CASE WHEN timedate_ms IS NOT NULL
         THEN epoch_ms(timedate_ms)::DATE END AS as_of_date
FROM "rbi-key-policy-rates"
WHERE name IS NOT NULL
  AND name NOT ILIKE '%Exchange Rate%'
  AND name NOT ILIKE '%CPI%'
  AND name NOT ILIKE '%Inflation%'
