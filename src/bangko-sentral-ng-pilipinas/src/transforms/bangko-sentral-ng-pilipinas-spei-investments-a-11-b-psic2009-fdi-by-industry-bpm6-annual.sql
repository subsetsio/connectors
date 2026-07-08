SELECT
    row_label,
    col_label,
    CAST(value AS DOUBLE) AS value,
    CAST(date AS DATE)    AS date
FROM "bangko-sentral-ng-pilipinas-spei-investments-a-11-b-psic2009-fdi-by-industry-bpm6-annual"
WHERE value IS NOT NULL
