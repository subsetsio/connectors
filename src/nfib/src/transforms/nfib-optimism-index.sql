SELECT
    date,
    optimism_index
FROM "nfib-optimism-index"
WHERE optimism_index IS NOT NULL
ORDER BY date
