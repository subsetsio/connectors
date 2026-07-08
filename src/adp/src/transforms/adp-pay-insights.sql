SELECT
    CAST(date AS DATE)        AS date,
    timestep                  AS frequency,
    aggregation,
    category,
    median_pay_change,
    median_annual_pay
FROM "adp-pay-insights"
WHERE date IS NOT NULL
