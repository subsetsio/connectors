-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CountyFP" AS countyfp,
    "County" AS county,
    "City" AS city,
    "County_Total_Sort" AS county_total_sort,
    "FIPS" AS fips,
    "FID" AS fid
FROM "california-department-of-finance-50a042556345443ab45d84716fadc43e"
