SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-da030f7028200d19ffcbe4a2d71af39c" WHERE month IS NOT NULL
