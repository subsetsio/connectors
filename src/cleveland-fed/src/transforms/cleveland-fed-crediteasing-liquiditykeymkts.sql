-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly (Wednesday) balance levels in millions of US dollars, not flows.
-- caution: `liquidity_to_key_credit_markets` is the total of the facility columns beside it — summing all columns double-counts.
-- caution: Facilities that did not exist in a given week carry 0, not null; a zero is 'programme inactive', not 'no observation'.
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
