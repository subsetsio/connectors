SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-56f64b2d5a31eb0ee465cc51e83ac60a" WHERE month IS NOT NULL
