-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "local_currency_code",
    "trade_country_name",
    "security_name",
    "security_description",
    "maturity_date",
    "interest_rate",
    "original_face",
    "sharespar_value",
    "base_market_value",
    "base_total_cost",
    "base_unrealized_gainloss",
    "base_accrued_interest",
    "local_market_value",
    "local_total_cost_amount",
    "local_unrealized_gainloss",
    "local_accrued_interest",
    "period_end_date",
    "asset_class",
    "investment_type_name",
    "major_industry_name",
    "minor_industry_name",
    "moodys_quality_rating",
    "s_and_p_quality_rating",
    "directgroup_trust_holding",
    "data_as_of"
FROM "nyc-open-data-fypi-ruxh"
