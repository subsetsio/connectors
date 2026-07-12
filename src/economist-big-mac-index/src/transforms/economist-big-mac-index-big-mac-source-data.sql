-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "iso_a3",
    "currency_code",
    "local_price",
    "dollar_ex",
    "GDP_dollar" AS gdp_dollar,
    "GDP_local" AS gdp_local,
    "date"
FROM "economist-big-mac-index-big-mac-source-data"
