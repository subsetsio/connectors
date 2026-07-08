SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-835d43b9238c6fc877dfcd62d73054a9" WHERE month IS NOT NULL
