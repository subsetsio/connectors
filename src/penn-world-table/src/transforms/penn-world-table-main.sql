SELECT
    * REPLACE (CAST(year AS INTEGER) AS year)
FROM "penn-world-table-main"
WHERE countrycode IS NOT NULL
  AND year IS NOT NULL
