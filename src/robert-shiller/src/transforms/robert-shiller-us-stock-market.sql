SELECT
    CAST(date AS DATE) AS date,
    CAST(sp500_price AS DOUBLE) AS sp500_price,
    CAST(dividend AS DOUBLE) AS dividend,
    CAST(earnings AS DOUBLE) AS earnings,
    CAST(cpi AS DOUBLE) AS cpi,
    CAST(long_interest_rate AS DOUBLE) AS long_interest_rate,
    CAST(real_price AS DOUBLE) AS real_price,
    CAST(real_dividend AS DOUBLE) AS real_dividend,
    CAST(real_total_return_price AS DOUBLE) AS real_total_return_price,
    CAST(real_earnings AS DOUBLE) AS real_earnings,
    CAST(real_tr_scaled_earnings AS DOUBLE) AS real_tr_scaled_earnings,
    CAST(cape AS DOUBLE) AS cape,
    CAST(tr_cape AS DOUBLE) AS tr_cape,
    CAST(excess_cape_yield AS DOUBLE) AS excess_cape_yield,
    CAST(monthly_total_bond_return AS DOUBLE) AS monthly_total_bond_return,
    CAST(real_total_bond_return AS DOUBLE) AS real_total_bond_return,
    CAST(real_stock_return_10y AS DOUBLE) AS real_stock_return_10y,
    CAST(real_bond_return_10y AS DOUBLE) AS real_bond_return_10y,
    CAST(excess_return_10y AS DOUBLE) AS excess_return_10y
FROM "robert-shiller-us-stock-market"
ORDER BY date
