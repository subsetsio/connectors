-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verifier did not find a compact unique grain; treat rows as report-specific statistical observations and filter all relevant dimensions before aggregating.
SELECT
    CAST("year" AS BIGINT) AS year,
    "economy",
    "economy_label",
    "flow",
    "flow_label",
    "us_at_current_prices_in_thousands",
    "us_at_current_prices_in_thousands_footnote",
    "us_at_current_prices_in_thousands_missing_value",
    "growth_rate_year_on_year",
    "growth_rate_year_on_year_footnote",
    "growth_rate_year_on_year_missing_value",
    "percentage_of_total_merchandise_trade",
    "percentage_of_total_merchandise_trade_footnote",
    "percentage_of_total_merchandise_trade_missing_value",
    "percentage_of_gross_domestic_product",
    "percentage_of_gross_domestic_product_footnote",
    "percentage_of_gross_domestic_product_missing_value"
FROM "unctad-us.wastewatertreatment"
