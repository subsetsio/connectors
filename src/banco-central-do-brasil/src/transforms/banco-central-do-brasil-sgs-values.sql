SELECT
    series_code,
    CAST(strptime(data, '%d/%m/%Y') AS DATE) AS date,
    TRY_CAST(valor AS DOUBLE)                AS value
FROM "banco-central-do-brasil-sgs-values"
WHERE valor IS NOT NULL AND valor <> ''
