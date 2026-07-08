SELECT
    country,
    CAST(date || '-01' AS DATE) AS date,
    holdings_billions
FROM "treasury-tic-mfh-treasury-holdings"
WHERE holdings_billions IS NOT NULL
