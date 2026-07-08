SELECT DISTINCT
    CAST(date AS DATE) AS date,
    CAST(price_pln_per_g AS DOUBLE) AS price_pln_per_g
FROM "narodowy-bank-polski-gold-prices"
WHERE price_pln_per_g IS NOT NULL
