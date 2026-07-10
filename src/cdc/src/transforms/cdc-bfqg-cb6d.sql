-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CCN" AS ccn,
    "Facility Name" AS facility_name,
    "Address" AS address,
    "City" AS city,
    "State" AS state,
    CAST("Zip Code" AS BIGINT) AS zip_code,
    CAST("Total Resident Weeks" AS BIGINT) AS total_resident_weeks,
    CAST("Total Covid Infections" AS BIGINT) AS total_covid_infections,
    CAST("Facility Infection Rate  Per 1000 Resident Weeks" AS DOUBLE) AS facility_infection_rate_per_1000_resident_weeks,
    CAST("County Infection Rate  Per 1000 Resident Weeks" AS DOUBLE) AS county_infection_rate_per_1000_resident_weeks,
    CAST("Infection Performance Score" AS DOUBLE) AS infection_performance_score,
    CAST("Infection Performance Score Capped" AS BIGINT) AS infection_performance_score_capped,
    CAST("Mortality Adjustment" AS DOUBLE) AS mortality_adjustment,
    "Performance Month" AS performance_month,
    CAST("Final Payment" AS BIGINT) AS final_payment
FROM "cdc-bfqg-cb6d"
