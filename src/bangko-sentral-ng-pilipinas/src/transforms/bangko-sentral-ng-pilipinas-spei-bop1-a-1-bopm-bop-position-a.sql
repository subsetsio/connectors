SELECT
    row_label,
    col_label,
    CAST(value AS DOUBLE) AS value,
    CAST(date AS DATE)    AS date
FROM "bangko-sentral-ng-pilipinas-spei-bop1-a-1-bopm-bop-position-a"
WHERE value IS NOT NULL
