SELECT DISTINCT
    CAST(date AS DATE)  AS date,
    CAST(wei AS DOUBLE) AS wei
FROM "dallas-fed-wei"
WHERE date IS NOT NULL AND wei IS NOT NULL
