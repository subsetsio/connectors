-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Provider Name" AS provider_name,
    "State" AS state,
    "City" AS city,
    "Payment" AS payment
FROM "cdc-kh8y-3es6"
