-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly (Wednesday) balance levels in millions of US dollars, not flows.
-- caution: `lending_to_financial_institutions` is the total of the facility columns beside it — summing all columns double-counts.
-- caution: Facilities that did not exist in a given week carry 0, not null; a zero is 'programme inactive', not 'no observation'.
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
