SELECT CAST(date AS DATE) AS date,
       partisan_conflict_index
FROM "philadelphia-fed-partisan-conflict-index"
WHERE partisan_conflict_index IS NOT NULL
ORDER BY date
