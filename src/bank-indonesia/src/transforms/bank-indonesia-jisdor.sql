SELECT DISTINCT
    CAST(date AS DATE) AS date,
    buy AS rate
FROM "bank-indonesia-jisdor"
WHERE date IS NOT NULL AND buy IS NOT NULL
