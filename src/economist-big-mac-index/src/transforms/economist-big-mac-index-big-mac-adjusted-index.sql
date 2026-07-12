-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GDP-adjusted index table is a column subset of the full index table; use the full index when raw and adjusted measures need to be compared in one query.
SELECT
    "date",
    "iso_a3",
    "currency_code",
    "name",
    "local_price",
    "dollar_ex",
    "dollar_price",
    "GDP_bigmac" AS gdp_bigmac,
    "adj_price",
    "USD" AS usd,
    "EUR" AS eur,
    "GBP" AS gbp,
    "JPY" AS jpy,
    "CNY" AS cny
FROM "economist-big-mac-index-big-mac-adjusted-index"
