-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "CCN" AS ccn,
    "Provider Name" AS provider_name,
    "City" AS city,
    "State" AS state,
    "Zip Code" AS zip_code,
    "FIPS County Code" AS fips_county_code,
    "County Name" AS county_name,
    "Report Date" AS report_date,
    "MDS Item Question/Description" AS mds_item_question_description,
    "MDS Item Response" AS mds_item_response,
    "Overall Percent" AS overall_percent,
    "Total Residents" AS total_residents,
    "Short-Stay Percent" AS short_stay_percent,
    "Short-Stay Residents" AS short_stay_residents,
    "Long-Stay Percent" AS long_stay_percent,
    "Long-Stay Residents" AS long_stay_residents
FROM "cms-d086edc0-4953-4fb9-a663-b35526371add"
