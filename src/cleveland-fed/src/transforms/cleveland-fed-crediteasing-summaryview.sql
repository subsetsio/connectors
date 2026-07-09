-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly (Wednesday) balance levels in millions of US dollars, not flows.
-- caution: The five programme columns are mutually exclusive components of the Federal Reserve's credit-easing balance sheet and each is the total of one of this source's detail tables; the row sum is total credit easing.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "lending_to_financial_institutions",
    "liquidity_to_key_credit_markets",
    "traditional_security_holdings",
    "federal_agency_debt_and_mortgage_backed_securities_purchases",
    "long_term_treasury_purchases"
FROM "cleveland-fed-crediteasing-summaryview"
