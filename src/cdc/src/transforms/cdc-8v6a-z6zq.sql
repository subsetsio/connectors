-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Provider Name" AS provider_name,
    "City" AS city,
    "State" AS state,
    CAST("ZIP" AS BIGINT) AS zip,
    "Payment" AS payment,
    "Rural Location" AS rural_location
FROM "cdc-8v6a-z6zq"
