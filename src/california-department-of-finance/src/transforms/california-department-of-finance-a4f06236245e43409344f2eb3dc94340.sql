-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "County" AS county,
    CAST("COUNTY_SORT" AS BIGINT) AS county_sort,
    "Housing_Type" AS housing_type,
    "Total_Fire_Loss" AS total_fire_loss,
    "ObjectId" AS objectid
FROM "california-department-of-finance-a4f06236245e43409344f2eb3dc94340"
