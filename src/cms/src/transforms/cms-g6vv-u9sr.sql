-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "Provider Name" AS provider_name,
    "Provider Address" AS provider_address,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "Penalty Date" AS penalty_date,
    "Penalty Type" AS penalty_type,
    "Fine ID" AS fine_id,
    "Fine Amount" AS fine_amount,
    "Payment Denial Start Date" AS payment_denial_start_date,
    "Payment Denial Length in Days" AS payment_denial_length_in_days,
    "Location" AS location,
    "Processing Date" AS processing_date
FROM "cms-g6vv-u9sr"
