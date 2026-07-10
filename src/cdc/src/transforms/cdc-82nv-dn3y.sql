-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Syphilis, Congenital§, Current week" AS BIGINT) AS syphilis_congenital_current_week,
    "Syphilis, Congenital§, Current week, flag" AS syphilis_congenital_current_week_flag,
    CAST("Syphilis, Congenital§, Previous 52 weeks Max†" AS BIGINT) AS syphilis_congenital_previous_52_weeks_max,
    "Syphilis, Congenital§, Previous 52 weeks Max†, flag" AS syphilis_congenital_previous_52_weeks_max_flag,
    CAST("Syphilis, Congenital§, Cum 2022†" AS BIGINT) AS syphilis_congenital_cum_2022,
    "Syphilis, Congenital§, Cum 2022†, flag" AS syphilis_congenital_cum_2022_flag,
    CAST("Syphilis, Congenital§, Cum 2021†" AS BIGINT) AS syphilis_congenital_cum_2021,
    "Syphilis, Congenital§, Cum 2021†, flag" AS syphilis_congenital_cum_2021_flag,
    CAST("Syphilis, Primary and secondary, Current week" AS BIGINT) AS syphilis_primary_and_secondary_current_week,
    "Syphilis, Primary and secondary, Current week, flag" AS syphilis_primary_and_secondary_current_week_flag,
    CAST("Syphilis, Primary and secondary, Previous 52 weeks Max†" AS BIGINT) AS syphilis_primary_and_secondary_previous_52_weeks_max,
    "Syphilis, Primary and secondary, Previous 52 weeks Max†, flag" AS syphilis_primary_and_secondary_previous_52_weeks_max_flag,
    CAST("Syphilis, Primary and secondary, Cum 2022†" AS BIGINT) AS syphilis_primary_and_secondary_cum_2022,
    "Syphilis, Primary and secondary, Cum 2022†, flag" AS syphilis_primary_and_secondary_cum_2022_flag,
    CAST("Syphilis, Primary and secondary, Cum 2021†" AS BIGINT) AS syphilis_primary_and_secondary_cum_2021,
    "Syphilis, Primary and secondary, Cum 2021†, flag" AS syphilis_primary_and_secondary_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-82nv-dn3y"
