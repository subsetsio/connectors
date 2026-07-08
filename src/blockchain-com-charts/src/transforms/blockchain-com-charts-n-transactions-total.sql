SELECT
    CAST(to_timestamp(x) AS TIMESTAMP) AS timestamp,
    CAST(y AS DOUBLE)                  AS value
FROM "blockchain-com-charts-n-transactions-total"
WHERE y IS NOT NULL
ORDER BY timestamp
