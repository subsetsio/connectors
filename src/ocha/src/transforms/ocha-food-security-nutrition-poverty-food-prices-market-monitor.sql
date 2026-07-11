-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are market price observations by commodity, market, currency, and period; compare prices only within compatible commodity_code, market_code, and currency_code values.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "resource_hdx_id",
    CAST("market_code" AS BIGINT) AS market_code,
    "market_name",
    CAST("commodity_code" AS BIGINT) AS commodity_code,
    "commodity_name",
    "commodity_category",
    "currency_code",
    "unit",
    "price_flag",
    "price_type",
    "price",
    "lat",
    "lon",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-food-security-nutrition-poverty-food-prices-market-monitor"
