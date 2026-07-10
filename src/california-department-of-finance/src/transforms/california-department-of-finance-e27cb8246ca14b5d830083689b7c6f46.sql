-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "County" AS county,
    "CO_FIPS" AS co_fips,
    "FIPS" AS fips,
    "Placecode" AS placecode,
    "Mobile_Home_Unit" AS mobile_home_unit,
    "Multi_Family_Structure" AS multi_family_structure,
    "Single_Family_Housing_Unit" AS single_family_housing_unit,
    "Grand_Total" AS grand_total,
    "ObjectId" AS objectid
FROM "california-department-of-finance-e27cb8246ca14b5d830083689b7c6f46"
