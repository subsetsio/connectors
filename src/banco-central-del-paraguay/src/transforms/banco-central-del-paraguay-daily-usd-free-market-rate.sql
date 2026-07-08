SELECT
    CAST(date AS DATE)  AS date,
    compra,
    venta
FROM "banco-central-del-paraguay-daily-usd-free-market-rate"
WHERE compra IS NOT NULL OR venta IS NOT NULL
