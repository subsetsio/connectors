SELECT
    CAST(year AS INTEGER) AS year,
    CAST(rank AS INTEGER) AS rank,
    company,
    country,
    CAST(arms_revenue_musd AS DOUBLE)    AS arms_revenue_musd,
    CAST(total_revenue_musd AS DOUBLE)   AS total_revenue_musd,
    CAST(arms_share_of_total AS DOUBLE)  AS arms_share_of_total
FROM "sipri-arms-industry-top100"
WHERE company IS NOT NULL
