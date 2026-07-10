-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source stores the quarter in the `month` column; treat the period as a quarter label, not a calendar month.
SELECT
    "month",
    "average",
    "year",
    "currencyCode" AS currencycode,
    "amount"
FROM "czech-national-bank-exrates-quarterly-averages"
