SELECT
    CAST(year AS INTEGER) AS year,
    CAST(total_arms_revenue_current_usd_bn AS DOUBLE) AS total_arms_revenue_current_usd_bn
FROM "sipri-arms-industry-total-revenues"
WHERE total_arms_revenue_current_usd_bn IS NOT NULL
