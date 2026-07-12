-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Historical 1986-1999 inputs contain price and exchange-rate fields only and predate the modern GDP-adjusted source fields.
SELECT
    "name",
    "iso_a3",
    "currency_code",
    "local_price",
    "dollar_ex",
    "date"
FROM "economist-big-mac-index-big-mac-historical-source-data"
