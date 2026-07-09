SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "repurchase_agreements",
    "term_auction_credit",
    "other_fed_assets",
    "securities_lent_to_dealers",
    "currency_swaps",
    "primary_credit",
    "secondary_credit",
    "seasonal_credit",
    "primary_other_broker_dealer",
    "credit_to_aig",
    "bank_term_funding_program",
    "other_credit",
    "ppp_liquidity_facility",
    "lending_to_financial_institutions"
FROM "cleveland-fed-crediteasing-lendingfincinst"
