SELECT
    asset,
    metric,
    CAST(date AS DATE) AS date,
    value
FROM (
    SELECT
        asset, metric, date, value,
        row_number() OVER (
            PARTITION BY asset, metric, date ORDER BY value
        ) AS rn
    FROM "coin-metrics-asset-metrics-values"
    WHERE value IS NOT NULL
)
WHERE rn = 1
