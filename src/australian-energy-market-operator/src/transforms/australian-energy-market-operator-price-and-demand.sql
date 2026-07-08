SELECT
    region,
    settlement_date,
    total_demand,
    rrp,
    period_type
FROM "australian-energy-market-operator-price-and-demand"
WHERE region IS NOT NULL
  AND settlement_date IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY region, settlement_date
    ORDER BY total_demand DESC NULLS LAST
) = 1
