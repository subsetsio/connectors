-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Hemolytic uremic snydrome post-diarrheal, Current week" AS BIGINT) AS hemolytic_uremic_snydrome_post_diarrheal_current_week,
    "Hemolytic uremic snydrome post-diarrheal, Current week, flag" AS hemolytic_uremic_snydrome_post_diarrheal_current_week_flag,
    CAST("Hemolytic uremic snydrome post-diarrheal, Previous 52 weeks Max†" AS BIGINT) AS hemolytic_uremic_snydrome_post_diarrheal_previous_52_weeks_max,
    "Hemolytic uremic snydrome post-diarrheal, Previous 52 weeks Max†, flag" AS hemolytic_uremic_snydrome_post_diarrheal_previous_52_weeks_max_flag,
    CAST("Hemolytic uremic snydrome post-diarrheal, Cum 2022†" AS BIGINT) AS hemolytic_uremic_snydrome_post_diarrheal_cum_2022,
    "Hemolytic uremic snydrome post-diarrheal, Cum 2022†, flag" AS hemolytic_uremic_snydrome_post_diarrheal_cum_2022_flag,
    CAST("Hemolytic uremic snydrome post-diarrheal, Cum 2021†" AS BIGINT) AS hemolytic_uremic_snydrome_post_diarrheal_cum_2021,
    "Hemolytic uremic snydrome post-diarrheal, Cum 2021†, flag" AS hemolytic_uremic_snydrome_post_diarrheal_cum_2021_flag,
    CAST("Hepatitis A, acute, Current week" AS BIGINT) AS hepatitis_a_acute_current_week,
    "Hepatitis A, acute, Current week, flag" AS hepatitis_a_acute_current_week_flag,
    CAST("Hepatitis A, acute, Previous 52 weeks Max†" AS BIGINT) AS hepatitis_a_acute_previous_52_weeks_max,
    "Hepatitis A, acute, Previous 52 weeks Max†, flag" AS hepatitis_a_acute_previous_52_weeks_max_flag,
    CAST("Hepatitis A, acute, Cum 2022†" AS BIGINT) AS hepatitis_a_acute_cum_2022,
    "Hepatitis A, acute, Cum 2022†, flag" AS hepatitis_a_acute_cum_2022_flag,
    CAST("Hepatitis A, acute, Cum 2021†" AS BIGINT) AS hepatitis_a_acute_cum_2021,
    "Hepatitis A, acute, Cum 2021†, flag" AS hepatitis_a_acute_cum_2021_flag,
    CAST("Hepatitis B, acute, Current week" AS BIGINT) AS hepatitis_b_acute_current_week,
    "Hepatitis B, acute, Current week, flag" AS hepatitis_b_acute_current_week_flag,
    CAST("Hepatitis B, acute, Previous 52 weeks Max†" AS BIGINT) AS hepatitis_b_acute_previous_52_weeks_max,
    "Hepatitis B, acute, Previous 52 weeks Max†, flag" AS hepatitis_b_acute_previous_52_weeks_max_flag,
    CAST("Hepatitis B, acute, Cum 2022†" AS BIGINT) AS hepatitis_b_acute_cum_2022,
    "Hepatitis B, acute, Cum 2022†, flag" AS hepatitis_b_acute_cum_2022_flag,
    CAST("Hepatitis B, acute, Cum 2021†" AS BIGINT) AS hepatitis_b_acute_cum_2021,
    "Hepatitis B, acute, Cum 2021†, flag" AS hepatitis_b_acute_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-ex65-qa8z"
