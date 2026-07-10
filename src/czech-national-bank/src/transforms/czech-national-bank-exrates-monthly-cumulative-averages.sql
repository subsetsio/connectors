-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly period values are year-to-date cumulative averages, not independent single-month averages.
SELECT
    "month",
    "average",
    "year",
    "currencyCode" AS currencycode,
    "amount"
FROM "czech-national-bank-exrates-monthly-cumulative-averages"
