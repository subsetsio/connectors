SELECT DISTINCT
    CAST(date AS DATE) AS date,
    code AS currency_code,
    currency AS currency_name,
    CAST(bid AS DOUBLE) AS bid,
    CAST(ask AS DOUBLE) AS ask
FROM "narodowy-bank-polski-exchange-rates-bid-ask"
WHERE bid IS NOT NULL AND ask IS NOT NULL
