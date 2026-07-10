-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "currencyCode" AS currencycode,
    "amount",
    "validFor" AS validfor,
    "rate"
FROM "czech-national-bank-exrates-daily"
