SELECT
    CAST(to_timestamp(x) AS TIMESTAMP) AS timestamp,
    CAST(y AS DOUBLE)                  AS value
FROM "blockchain-com-charts-transaction-fees"
WHERE y IS NOT NULL
ORDER BY timestamp
