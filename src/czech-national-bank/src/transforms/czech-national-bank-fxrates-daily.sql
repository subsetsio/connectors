-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "validFor" AS validfor,
    "order",
    "country",
    "currency",
    "amount",
    "currencyCode" AS currencycode,
    "rate"
FROM "czech-national-bank-fxrates-daily"
