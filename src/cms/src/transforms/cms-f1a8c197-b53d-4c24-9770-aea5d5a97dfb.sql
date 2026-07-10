-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "NPI" AS npi,
    "PROVIDER NAME" AS provider_name,
    "ADDRESS LINE 1" AS address_line_1,
    "ADDRESS LINE 2" AS address_line_2,
    "CITY" AS city,
    "STATE" AS state,
    "ZIP" AS zip,
    strptime("MEDICARE ID EFFECTIVE DATE", '%m/%d/%Y')::DATE AS medicare_id_effective_date,
    "PHONE" AS phone
FROM "cms-f1a8c197-b53d-4c24-9770-aea5d5a97dfb"
