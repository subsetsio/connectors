-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "ACO_ID" AS aco_id,
    CAST("year" AS BIGINT) AS year,
    "STATE_ID" AS state_id,
    "COUNTY_ID" AS county_id,
    "STATE_NAME" AS state_name,
    "COUNTY_NAME" AS county_name,
    "ELIG_MONTHS_AD" AS elig_months_ad,
    "ELIG_MONTHS_ESRD" AS elig_months_esrd,
    "ELIG_MONTHS_TOTAL" AS elig_months_total,
    "ALIGNED_BENEFICIARIES_AD" AS aligned_beneficiaries_ad,
    "ALIGNED_BENEFICIARIES_ESRD" AS aligned_beneficiaries_esrd
FROM "cms-1cd9eded-d2c9-4215-a064-aac6dae3b714"
