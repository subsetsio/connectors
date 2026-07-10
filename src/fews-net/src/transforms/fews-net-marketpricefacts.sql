-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix countries, markets, products, price types, currencies, units, and normalized price fields; filter those dimensions before comparing or aggregating prices.
SELECT
    "id",
    "country",
    "admin_1",
    "admin_2",
    "market",
    "cpcv2",
    "product",
    "price_type",
    "product_source",
    "period_date",
    "start_date",
    "value",
    "currency",
    "unit",
    "common_unit",
    "common_currency",
    "common_unit_price",
    "common_currency_price"
FROM "fews-net-marketpricefacts"
