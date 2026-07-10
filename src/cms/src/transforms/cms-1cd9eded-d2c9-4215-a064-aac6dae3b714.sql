-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "aco_id",
    CAST("year" AS BIGINT) AS year,
    "state_id",
    "county_id",
    "state_name",
    "county_name",
    "elig_months_ad",
    "elig_months_esrd",
    "elig_months_total",
    "aligned_beneficiaries_ad",
    "aligned_beneficiaries_esrd"
FROM "cms-1cd9eded-d2c9-4215-a064-aac6dae3b714"
