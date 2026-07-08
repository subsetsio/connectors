SELECT
    CAST(date AS DATE) AS date,
    country,
    state,
    classification,
    salary_sa_index,
    salary_sa_growth_month,
    salary_sa_growth_pcp,
    salary_trend_index,
    salary_trend_growth_month,
    salary_trend_growth_pcp
FROM "seek-advertised-salary-index"
WHERE salary_sa_index IS NOT NULL OR salary_trend_index IS NOT NULL
