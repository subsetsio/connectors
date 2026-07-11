-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Self-service machine locator rows can repeat across address, machine type, service hours, and coordinates; the source does not publish a stable row identifier, so the pass-through table is intentionally keyless.
SELECT
    "district",
    "bank_name",
    "type_of_machine",
    "address",
    "service_hours",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude
FROM "hkma-bank-ssm"
