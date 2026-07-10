-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "County" AS county,
    "City" AS city,
    "FIPS" AS fips,
    CAST("Year" AS BIGINT) AS year,
    "Year123" AS year123,
    "Total_Net_Annual_Housing_Unit_C" AS total_net_annual_housing_unit_c,
    "Total_Net_Annual_Affordable_Hou" AS total_net_annual_affordable_hou,
    "Total_Housing_Unit_Change_Perce" AS total_housing_unit_change_perce,
    "SubCounty" AS subcounty,
    "Sub" AS sub,
    "textJurisdiction" AS textjurisdiction,
    "BannerName" AS bannername,
    "Total_Net_Annual_Housing_Unit_1" AS total_net_annual_housing_unit_1,
    "Total_Net_Annual_Affordable_H_1" AS total_net_annual_affordable_h_1,
    "FID" AS fid,
    "PercentAFU" AS percentafu
FROM "california-department-of-finance-bc1cfb5ef50a43a9b60e25c11c32255b"
