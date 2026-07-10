-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Facility ID" AS facility_id,
    "Facility Name" AS facility_name,
    "Address" AS address,
    "City/Town" AS city_town,
    "State" AS state,
    CAST("ZIP Code" AS BIGINT) AS zip_code,
    "County/Parish" AS county_parish,
    "Telephone Number" AS telephone_number,
    "Measure ID" AS measure_id,
    "Measure Name" AS measure_name,
    "Compared to National" AS compared_to_national,
    "Denominator" AS denominator,
    "Score" AS score,
    "Lower Estimate" AS lower_estimate,
    "Higher Estimate" AS higher_estimate,
    "Footnote" AS footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-zez1-ka2w"
