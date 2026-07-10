-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PROVIDER NAME" AS provider_name,
    "CITY" AS city,
    "STATE" AS state,
    CAST("CLAIMS PAID FOR VACCINE" AS BIGINT) AS claims_paid_for_vaccine
FROM "cdc-xgy8-wnft"
