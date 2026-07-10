-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Provider Name" AS provider_name,
    "State / Territory" AS state_territory,
    CAST("Provider Relief Fund" AS DOUBLE) AS provider_relief_fund,
    CAST("AAP" AS DOUBLE) AS aap
FROM "cdc-v2pi-w3up"
