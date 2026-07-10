-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "First Name" AS first_name,
    "Last Name" AS last_name,
    CAST("npi" AS BIGINT) AS npi,
    "Specialty" AS specialty,
    strptime("Optout Effective Date", '%m/%d/%Y')::DATE AS optout_effective_date,
    strptime("Optout End Date", '%m/%d/%Y')::DATE AS optout_end_date,
    "First Line Street Address" AS first_line_street_address,
    "Second Line Street Address" AS second_line_street_address,
    "City Name" AS city_name,
    "State Code" AS state_code,
    "Zip code" AS zip_code,
    "Eligible to Order and Refer" AS eligible_to_order_and_refer,
    strptime("Last updated", '%m/%d/%Y')::DATE AS last_updated
FROM "cms-9887a515-7552-4693-bf58-735c77af46d7"
