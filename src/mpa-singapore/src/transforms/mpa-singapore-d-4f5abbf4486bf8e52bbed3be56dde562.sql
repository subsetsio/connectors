SELECT CAST(strptime(month, '%Y-%m') AS DATE) AS date, * EXCLUDE (month) FROM "mpa-singapore-d-4f5abbf4486bf8e52bbed3be56dde562" WHERE month IS NOT NULL
