SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-89d2874dad74a273270369334f1e7d28" WHERE month IS NOT NULL
