SELECT
    CAST(cik AS BIGINT) AS cik,
    name,
    ticker,
    exchange
FROM "sec-companies"
WHERE cik IS NOT NULL
