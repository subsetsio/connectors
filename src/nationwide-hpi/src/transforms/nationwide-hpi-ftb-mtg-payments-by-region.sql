SELECT
    CAST(date AS DATE)    AS date,
    period_label,
    category,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "nationwide-hpi-ftb-mtg-payments-by-region"
WHERE value IS NOT NULL
