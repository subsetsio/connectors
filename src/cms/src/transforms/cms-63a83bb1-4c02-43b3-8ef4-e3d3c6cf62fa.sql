-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "NPI" AS npi,
    "Provider Name" AS provider_name
FROM "cms-63a83bb1-4c02-43b3-8ef4-e3d3c6cf62fa"
