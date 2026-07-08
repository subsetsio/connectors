SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-c9dcfd8b85990669d1e74dd7ad71eb8b" WHERE month IS NOT NULL
