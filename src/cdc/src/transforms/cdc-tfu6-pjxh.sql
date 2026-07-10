-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Tuberculosis, Current week" AS BIGINT) AS tuberculosis_current_week,
    "Tuberculosis, Current week, flag" AS tuberculosis_current_week_flag,
    CAST("Tuberculosis, Previous 52 weeks Max†" AS BIGINT) AS tuberculosis_previous_52_weeks_max,
    "Tuberculosis, Previous 52 weeks Max†, flag" AS tuberculosis_previous_52_weeks_max_flag,
    CAST("Tuberculosis, Cum 2022†" AS BIGINT) AS tuberculosis_cum_2022,
    "Tuberculosis, Cum 2022†, flag" AS tuberculosis_cum_2022_flag,
    CAST("Tuberculosis, Cum 2021†" AS BIGINT) AS tuberculosis_cum_2021,
    "Tuberculosis, Cum 2021†, flag" AS tuberculosis_cum_2021_flag,
    "Tularemia, Current week" AS tularemia_current_week,
    "Tularemia, Current week, flag" AS tularemia_current_week_flag,
    CAST("Tularemia, Previous 52 weeks Max†" AS BIGINT) AS tularemia_previous_52_weeks_max,
    "Tularemia, Previous 52 weeks Max†, flag" AS tularemia_previous_52_weeks_max_flag,
    "Tularemia, Cum 2022†" AS tularemia_cum_2022,
    "Tularemia, Cum 2022†, flag" AS tularemia_cum_2022_flag,
    "Tularemia, Cum 2021†" AS tularemia_cum_2021,
    "Tularemia, Cum 2021†, flag" AS tularemia_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-tfu6-pjxh"
