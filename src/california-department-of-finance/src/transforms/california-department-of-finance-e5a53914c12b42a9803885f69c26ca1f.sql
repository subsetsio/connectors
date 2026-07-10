-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: County-level urban classification table stores decade and post-threshold change measures as separate columns.
SELECT
    "County_Name" AS county_name,
    "CountyFP" AS countyfp,
    "F2010_Census_Total_Population" AS f2010_census_total_population,
    "F2010_Census_Urban_Population" AS f2010_census_urban_population,
    "F2010_Census_Percent_of_Total_P" AS f2010_census_percent_of_total_p,
    "F2020_Census_Total_Population" AS f2020_census_total_population,
    "Change__2010_to_2020" AS change_2010_to_2020,
    "F2020_Census_Urban_Population" AS f2020_census_urban_population,
    "F2020_Census_Percent_of_Total_P" AS f2020_census_percent_of_total_p,
    "Change_in_Urban_Population" AS change_in_urban_population,
    "Percent_Change_in_Urban_Populat" AS percent_change_in_urban_populat,
    "ObjectId" AS objectid
FROM "california-department-of-finance-e5a53914c12b42a9803885f69c26ca1f"
