SELECT
    * REPLACE (CAST(year AS INTEGER) AS year)
FROM "penn-world-table-capital-detail"
WHERE countrycode IS NOT NULL
  AND year IS NOT NULL
