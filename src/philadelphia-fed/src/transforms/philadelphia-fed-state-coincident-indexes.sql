SELECT CAST(date AS DATE) AS date,
       state,
       coincident_index
FROM "philadelphia-fed-state-coincident-indexes"
WHERE coincident_index IS NOT NULL
ORDER BY date, state
