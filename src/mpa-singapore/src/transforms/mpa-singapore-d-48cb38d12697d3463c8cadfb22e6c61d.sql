SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-48cb38d12697d3463c8cadfb22e6c61d" WHERE month IS NOT NULL
