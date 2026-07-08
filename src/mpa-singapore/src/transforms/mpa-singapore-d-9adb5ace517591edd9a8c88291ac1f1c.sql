SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-9adb5ace517591edd9a8c88291ac1f1c" WHERE month IS NOT NULL
