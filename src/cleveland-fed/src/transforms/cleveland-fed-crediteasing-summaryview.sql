SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "lending_to_financial_institutions",
    "liquidity_to_key_credit_markets",
    "traditional_security_holdings",
    "federal_agency_debt_and_mortgage_backed_securities_purchases",
    "long_term_treasury_purchases"
FROM "cleveland-fed-crediteasing-summaryview"
