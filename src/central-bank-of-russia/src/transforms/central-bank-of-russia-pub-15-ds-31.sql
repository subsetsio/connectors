SELECT DISTINCT
    CAST(date AS DATE)        AS date,
    periodicity,
    measure_name              AS measure,
    element_name              AS series,
    unit,
    CAST(obs_val AS DOUBLE)   AS value
FROM "central-bank-of-russia-pub-15-ds-31"
WHERE obs_val IS NOT NULL
