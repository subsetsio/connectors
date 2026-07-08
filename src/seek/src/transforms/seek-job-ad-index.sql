SELECT
    CAST(date AS DATE) AS date,
    country,
    state,
    ads_sa_index,
    ads_trend_index,
    ads_sa_growth_month,
    ads_sa_growth_pcp,
    ads_trend_growth_month,
    ads_trend_growth_pcp
FROM "seek-job-ad-index"
WHERE ads_sa_index IS NOT NULL OR ads_trend_index IS NOT NULL
