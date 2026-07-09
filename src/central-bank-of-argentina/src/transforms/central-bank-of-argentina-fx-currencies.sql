SELECT DISTINCT
    codigo       AS currency_code,
    denominacion AS currency_name
FROM "central-bank-of-argentina-fx-currencies"
WHERE codigo IS NOT NULL
