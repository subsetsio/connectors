SELECT
    * REPLACE (CAST(year AS INTEGER) AS year)
FROM "penn-world-table-na-data"
WHERE countrycode IS NOT NULL
  AND year IS NOT NULL
