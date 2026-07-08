SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-d48c5a038904f6da3c603cd854b6c191" WHERE month IS NOT NULL
