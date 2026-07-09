SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "asset_backed_commercial_paper",
    "term_asset_backed_securities",
    "net_portfolio_commercial_paper",
    "maiden_lane_1",
    "maiden_lane_2",
    "maiden_lane_3",
    "money_market_mutual_funds",
    "corporate_credit_facility",
    "municipal_liquidity_facility",
    "main_street_lending_facility",
    "liquidity_to_key_credit_markets"
FROM "cleveland-fed-crediteasing-liquiditykeymkts"
