-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: (`currency`, `ratedate`) is NOT unique: 116 currency-days carry more than one quote, most of them divergent (e.g. two different EURO rates for 2026-05-25). Pick one row per currency-day before charting or joining.
-- caution: The `currency` domain is dirty in two ways: values carry trailing spaces and tabs, and the same currency appears under several names over time (`YEN` vs `JAPANESE YEN`, `POUND STERLING` vs `POUNDS STERLING`, `DANISH KRONA` vs `DANISH KRONER`). Trim and alias before grouping by currency, or one currency splits into several series.
-- caution: The domain also contains `NAIRA` (the quote currency itself) and `POESO`, which are not ordinary foreign-currency quotes.
-- caution: Rates are naira per one unit of the foreign currency, so they are not comparable in magnitude across currencies.
SELECT
    "id",
    "currency",
    "ratedate",
    CAST("buyingrate" AS DOUBLE) AS buyingrate,
    CAST("centralrate" AS DOUBLE) AS centralrate,
    CAST("sellingrate" AS DOUBLE) AS sellingrate
FROM "central-bank-of-nigeria-exchange-rates-daily"
