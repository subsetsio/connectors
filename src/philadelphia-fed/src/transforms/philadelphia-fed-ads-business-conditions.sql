SELECT CAST(date AS DATE) AS date,
       ads_index,
       recession_bar
FROM "philadelphia-fed-ads-business-conditions"
WHERE ads_index IS NOT NULL
ORDER BY date
