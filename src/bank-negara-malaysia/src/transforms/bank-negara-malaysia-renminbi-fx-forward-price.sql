SELECT CAST(date AS DATE) AS date, * EXCLUDE (date)
FROM "bank-negara-malaysia-renminbi-fx-forward-price"
WHERE date IS NOT NULL
