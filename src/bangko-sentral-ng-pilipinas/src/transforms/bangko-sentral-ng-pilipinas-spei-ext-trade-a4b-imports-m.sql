SELECT
    row_label,
    col_label,
    CAST(value AS DOUBLE) AS value,
    CAST(date AS DATE)    AS date
FROM "bangko-sentral-ng-pilipinas-spei-ext-trade-a4b-imports-m"
WHERE value IS NOT NULL
