SELECT
    make_date(year, month, 1) AS date,
    series,
    CAST(value AS DOUBLE)      AS value
FROM "umich-surveys-of-consumers-table-42"
WHERE value IS NOT NULL
ORDER BY date, series
