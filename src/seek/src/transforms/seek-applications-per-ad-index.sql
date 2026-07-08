SELECT
    CAST(date AS DATE) AS date,
    country,
    state,
    ca_sa_index,
    ca_trend_index,
    ca_sa_growth_month,
    ca_sa_growth_pcp,
    ca_trend_growth_month,
    ca_trend_growth_pcp
FROM "seek-applications-per-ad-index"
WHERE ca_sa_index IS NOT NULL OR ca_trend_index IS NOT NULL
