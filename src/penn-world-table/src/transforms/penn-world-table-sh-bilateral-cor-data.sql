SELECT
    * REPLACE (CAST(year AS INTEGER) AS year)
FROM "penn-world-table-sh-bilateral-cor-data"
WHERE countrycode1 IS NOT NULL
  AND countrycode2 IS NOT NULL
  AND year IS NOT NULL
