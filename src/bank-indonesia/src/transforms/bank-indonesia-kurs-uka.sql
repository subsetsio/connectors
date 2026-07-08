SELECT DISTINCT
    CAST(date AS DATE) AS date,
    currency,
    unit,
    buy  AS buy_rate,
    sell AS sell_rate
FROM "bank-indonesia-kurs-uka"
WHERE date IS NOT NULL AND currency IS NOT NULL
  AND buy > 0 AND sell > 0
