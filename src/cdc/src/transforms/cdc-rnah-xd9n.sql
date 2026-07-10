-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Hepatitis C, perinatal infection, Current week" AS hepatitis_c_perinatal_infection_current_week,
    "Hepatitis C, perinatal infection, Current week, flag" AS hepatitis_c_perinatal_infection_current_week_flag,
    CAST("Hepatitis C, perinatal infection, Previous 52 weeks Max†" AS BIGINT) AS hepatitis_c_perinatal_infection_previous_52_weeks_max,
    "Hepatitis C, perinatal infection, Previous 52 weeks Max†, flag" AS hepatitis_c_perinatal_infection_previous_52_weeks_max_flag,
    "Hepatitis C, perinatal infection, Cum 2022†" AS hepatitis_c_perinatal_infection_cum_2022,
    "Hepatitis C, perinatal infection, Cum 2022†, flag" AS hepatitis_c_perinatal_infection_cum_2022_flag,
    CAST("Hepatitis C, perinatal infection, Cum 2021†" AS BIGINT) AS hepatitis_c_perinatal_infection_cum_2021,
    "Hepatitis C, perinatal infection, Cum 2021†, flag" AS hepatitis_c_perinatal_infection_cum_2021_flag,
    "Influenza-associated pediatric mortality§, Current week" AS influenza_associated_pediatric_mortality_current_week,
    "Influenza-associated pediatric mortality§, Current week, flag" AS influenza_associated_pediatric_mortality_current_week_flag,
    CAST("Influenza-associated pediatric mortality§, Previous 52 weeks Max†" AS BIGINT) AS influenza_associated_pediatric_mortality_previous_52_weeks_max,
    "Influenza-associated pediatric mortality§, Previous 52 weeks Max†, flag" AS influenza_associated_pediatric_mortality_previous_52_weeks_max_flag,
    "Influenza-associated pediatric mortality§, Cum 2022†" AS influenza_associated_pediatric_mortality_cum_2022,
    "Influenza-associated pediatric mortality§, Cum 2022†, flag" AS influenza_associated_pediatric_mortality_cum_2022_flag,
    "Influenza-associated pediatric mortality§, Cum 2021†" AS influenza_associated_pediatric_mortality_cum_2021,
    "Influenza-associated pediatric mortality§, Cum 2021†, flag" AS influenza_associated_pediatric_mortality_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-rnah-xd9n"
