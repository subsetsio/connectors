SELECT
    row_label,
    col_label,
    CAST(value AS DOUBLE) AS value,
    CAST(date AS DATE)    AS date
FROM "bangko-sentral-ng-pilipinas-spei-ext-accts-bop3-investments"
WHERE value IS NOT NULL
