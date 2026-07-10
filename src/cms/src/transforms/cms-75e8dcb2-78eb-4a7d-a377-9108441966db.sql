-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "LAST_NAME" AS last_name,
    "FIRST_NAME" AS first_name
FROM "cms-75e8dcb2-78eb-4a7d-a377-9108441966db"
