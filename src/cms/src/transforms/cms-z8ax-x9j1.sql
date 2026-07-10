-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Facility ID" AS facility_id,
    "Facility Name" AS facility_name,
    "Hospital Type" AS hospital_type,
    "Address" AS address,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "County/Parish" AS county_parish,
    "Measure ID" AS measure_id,
    "Measure Description" AS measure_description,
    "Total Cases" AS total_cases,
    "Performance Category" AS performance_category,
    "Rate" AS rate,
    "Interval Lower Limit" AS interval_lower_limit,
    "Interval Upper Limit" AS interval_upper_limit,
    "Footnote" AS footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-z8ax-x9j1"
