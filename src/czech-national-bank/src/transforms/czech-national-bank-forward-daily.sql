-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "validFor" AS validfor,
    "ccyPair" AS ccypair,
    "maturity",
    "forwardPoints" AS forwardpoints
FROM "czech-national-bank-forward-daily"
