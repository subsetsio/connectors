-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a current-year change snapshot rather than a full annual history; `Date` is the source's release/period code.
SELECT
    "Placecode" AS placecode,
    "FIPS" AS fips,
    "COUNTY" AS county,
    "F__CITY" AS f_city,
    "City2" AS city2,
    "Date" AS date,
    "Total_Population" AS total_population,
    "Household_Population" AS household_population,
    "Group_Quarters_Population" AS group_quarters_population,
    "Total_Housing_Units" AS total_housing_units,
    "PercentChangeTotal_Population" AS percentchangetotal_population,
    "PercentChangeHousehold_Populati" AS percentchangehousehold_populati,
    "PercentChangeGroup_Quarters_Pop" AS percentchangegroup_quarters_pop,
    "PercentChangeTotal_Housing_Unit" AS percentchangetotal_housing_unit,
    "FID" AS fid,
    "sort"
FROM "california-department-of-finance-11fd91ff08f04c618b2f87bec2a1a420"
