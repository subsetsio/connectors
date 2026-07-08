SELECT
    row_label,
    col_label,
    CAST(value AS DOUBLE) AS value,
    CAST(date AS DATE)    AS date
FROM "bangko-sentral-ng-pilipinas-spei-investments-a-11-a-foreign-direct-investment-bpm6-quarterly"
WHERE value IS NOT NULL
