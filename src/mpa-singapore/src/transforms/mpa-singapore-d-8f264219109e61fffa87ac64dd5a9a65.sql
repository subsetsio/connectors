SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-8f264219109e61fffa87ac64dd5a9a65" WHERE month IS NOT NULL
