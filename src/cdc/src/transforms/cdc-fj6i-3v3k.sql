-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Hepatitis B, perinatal infection, Current week" AS hepatitis_b_perinatal_infection_current_week,
    "Hepatitis B, perinatal infection, Current week, flag" AS hepatitis_b_perinatal_infection_current_week_flag,
    CAST("Hepatitis B, perinatal infection, Previous 52 weeks Max†" AS BIGINT) AS hepatitis_b_perinatal_infection_previous_52_weeks_max,
    "Hepatitis B, perinatal infection, Previous 52 weeks Max† , flag" AS hepatitis_b_perinatal_infection_previous_52_weeks_max_flag,
    "Hepatitis B, perinatal infection, Cum 2022†" AS hepatitis_b_perinatal_infection_cum_2022,
    "Hepatitis B, perinatal infection, Cum 2022†, flag" AS hepatitis_b_perinatal_infection_cum_2022_flag,
    CAST("Hepatitis B, perinatal infection, Cum 2021†" AS BIGINT) AS hepatitis_b_perinatal_infection_cum_2021,
    "Hepatitis B, perinatal infection, Cum 2021†, flag" AS hepatitis_b_perinatal_infection_cum_2021_flag,
    CAST("Hepatitis C, acute§, Confirmed, Current week" AS BIGINT) AS hepatitis_c_acute_confirmed_current_week,
    "Hepatitis C, acute§, Confirmed, Current week, flag" AS hepatitis_c_acute_confirmed_current_week_flag,
    CAST("Hepatitis C, acute§, Confirmed, Previous 52 weeks Max†" AS BIGINT) AS hepatitis_c_acute_confirmed_previous_52_weeks_max,
    "Hepatitis C, acute§, Previous 52 weeks Max† , flag" AS hepatitis_c_acute_previous_52_weeks_max_flag,
    CAST("Hepatitis C, acute§, Confirmed, Cum 2022†" AS BIGINT) AS hepatitis_c_acute_confirmed_cum_2022,
    "Hepatitis C, acute§, Confirmed, Cum 2022†, flag" AS hepatitis_c_acute_confirmed_cum_2022_flag,
    CAST("Hepatitis C, acute§, Confirmed, Cum 2021†" AS BIGINT) AS hepatitis_c_acute_confirmed_cum_2021,
    "Hepatitis C, acute§, Confirmed, Cum 2021†, flag" AS hepatitis_c_acute_confirmed_cum_2021_flag,
    CAST("Hepatitis C, acute§, Probable, Current week" AS BIGINT) AS hepatitis_c_acute_probable_current_week,
    "Hepatitis C, acute§, Probable, Current week, flag" AS hepatitis_c_acute_probable_current_week_flag,
    CAST("Hepatitis C, acute§, Probable, Previous 52 weeks Max†" AS BIGINT) AS hepatitis_c_acute_probable_previous_52_weeks_max,
    "Hepatitis C, acute§, Probable, Previous 52 weeks Max† , flag" AS hepatitis_c_acute_probable_previous_52_weeks_max_flag,
    CAST("Hepatitis C, acute§, Probable, Cum 2022†" AS BIGINT) AS hepatitis_c_acute_probable_cum_2022,
    "Hepatitis C, acute§, Probable, Cum 2022†, flag" AS hepatitis_c_acute_probable_cum_2022_flag,
    CAST("Hepatitis C, acute§, Probable, Cum 2021†" AS BIGINT) AS hepatitis_c_acute_probable_cum_2021,
    "Hepatitis C, acute§, Probable, Cum 2021†, flag" AS hepatitis_c_acute_probable_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-fj6i-3v3k"
