SELECT
    signalname AS predictor,
    port,
    CAST(date AS DATE) AS date,
    CAST(ret AS DOUBLE) AS ret,
    CAST(signallag AS DOUBLE) AS signal_lag,
    CAST(Nlong AS BIGINT) AS n_long,
    CAST(Nshort AS BIGINT) AS n_short
FROM "open-source-asset-pricing-portfolio-sorts"
WHERE ret IS NOT NULL
