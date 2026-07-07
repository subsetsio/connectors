SELECT
    strptime(CAST(fecha AS VARCHAR), '%d/%m/%Y')::DATE AS date,
    CAST(moneda AS INTEGER)                            AS currency_id,
    CAST(compra AS DOUBLE)                             AS buy_rate,
    CAST(venta AS DOUBLE)                              AS sell_rate
FROM "banco-de-guatemala-exchange-rates"
WHERE fecha IS NOT NULL
  AND moneda IS NOT NULL
  AND (compra IS NOT NULL OR venta IS NOT NULL)
