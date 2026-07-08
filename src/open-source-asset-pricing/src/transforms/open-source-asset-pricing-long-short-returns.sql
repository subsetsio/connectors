SELECT
    CAST(date AS DATE) AS date,
    predictor,
    CAST(ret AS DOUBLE) AS ret
FROM "open-source-asset-pricing-long-short-returns"
WHERE ret IS NOT NULL
