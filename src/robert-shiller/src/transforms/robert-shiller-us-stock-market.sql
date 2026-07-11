-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Forward 10-year return columns are unavailable for recent observations because their full future return window has not elapsed.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "sp500_price",
    "dividend",
    "earnings",
    "cpi",
    "long_interest_rate",
    "real_price",
    "real_dividend",
    "real_total_return_price",
    "real_earnings",
    "real_tr_scaled_earnings",
    "cape",
    "tr_cape",
    "excess_cape_yield",
    "monthly_total_bond_return",
    "real_total_bond_return",
    "real_stock_return_10y",
    "real_bond_return_10y",
    "excess_return_10y"
FROM "robert-shiller-us-stock-market"
