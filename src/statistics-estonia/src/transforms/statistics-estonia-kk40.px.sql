-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "environmental_protection_and_resource_management_activity",
    "receiving_sector",
    "paying_sector",
    "esa_transfers_type",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-kk40.px"
