-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Smallpox, Current week" AS smallpox_current_week,
    "Smallpox, Current week, flag" AS smallpox_current_week_flag,
    CAST("Smallpox, Previous 52 weeks Max†" AS BIGINT) AS smallpox_previous_52_weeks_max,
    "Smallpox, Previous 52 weeks Max†, flag" AS smallpox_previous_52_weeks_max_flag,
    "Smallpox, Cum 2022†" AS smallpox_cum_2022,
    "Smallpox, Cum 2022†, flag" AS smallpox_cum_2022_flag,
    "Smallpox, Cum 2021†" AS smallpox_cum_2021,
    "Smallpox, Cum 2021†, flag" AS smallpox_cum_2021_flag,
    CAST("Streptococcal toxic shock syndrome, Current week" AS BIGINT) AS streptococcal_toxic_shock_syndrome_current_week,
    "Streptococcal toxic shock syndrome, Current week, flag" AS streptococcal_toxic_shock_syndrome_current_week_flag,
    CAST("Streptococcal toxic shock syndrome, Previous 52 weeks Max†" AS BIGINT) AS streptococcal_toxic_shock_syndrome_previous_52_weeks_max,
    "Streptococcal toxic shock syndrome, Previous 52 weeks Max†, flag" AS streptococcal_toxic_shock_syndrome_previous_52_weeks_max_flag,
    CAST("Streptococcal toxic shock syndrome, Cum 2022†" AS BIGINT) AS streptococcal_toxic_shock_syndrome_cum_2022,
    "Streptococcal toxic shock syndrome, Cum 2022†, flag" AS streptococcal_toxic_shock_syndrome_cum_2022_flag,
    CAST("Streptococcal toxic shock syndrome, Cum 2021†" AS BIGINT) AS streptococcal_toxic_shock_syndrome_cum_2021,
    "Streptococcal toxic shock syndrome, Cum 2021†, flag" AS streptococcal_toxic_shock_syndrome_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-uw7a-a5t8"
