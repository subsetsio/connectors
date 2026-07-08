SELECT DISTINCT
    CAST(idVariable AS BIGINT) AS variable_id,
    CAST(fecha AS DATE)        AS date,
    CAST(valor AS DOUBLE)      AS value
FROM "central-bank-of-argentina-monetary-values"
WHERE valor IS NOT NULL AND fecha IS NOT NULL
