-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Facility Name" AS facility_name,
    "Facility ID" AS facility_id,
    "State" AS state,
    "Period" AS period,
    "Claim Type" AS claim_type,
    CAST("Avg Spndg Per EP Hospital" AS BIGINT) AS avg_spndg_per_ep_hospital,
    CAST("Avg Spndg Per EP State" AS BIGINT) AS avg_spndg_per_ep_state,
    CAST("Avg Spndg Per EP National" AS BIGINT) AS avg_spndg_per_ep_national,
    "Percent of Spndg Hospital" AS percent_of_spndg_hospital,
    "Percent of Spndg State" AS percent_of_spndg_state,
    "Percent of Spndg National" AS percent_of_spndg_national,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-nrth-mfg3"
