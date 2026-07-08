SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-042dd8b935eab998f389adaf559c80de" WHERE month IS NOT NULL
