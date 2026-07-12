-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the canonical combined index table and includes columns also published in the raw-index and adjusted-index subset tables.
SELECT
    "date",
    "iso_a3",
    "currency_code",
    "name",
    "local_price",
    "dollar_ex",
    "dollar_price",
    "USD_raw" AS usd_raw,
    "EUR_raw" AS eur_raw,
    "GBP_raw" AS gbp_raw,
    "JPY_raw" AS jpy_raw,
    "CNY_raw" AS cny_raw,
    "GDP_bigmac" AS gdp_bigmac,
    "adj_price",
    "USD_adjusted" AS usd_adjusted,
    "EUR_adjusted" AS eur_adjusted,
    "GBP_adjusted" AS gbp_adjusted,
    "JPY_adjusted" AS jpy_adjusted,
    "CNY_adjusted" AS cny_adjusted
FROM "economist-big-mac-index-big-mac-full-index"
