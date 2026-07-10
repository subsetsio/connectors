-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Malaria, Current week" AS BIGINT) AS malaria_current_week,
    "Malaria, Current week, flag" AS malaria_current_week_flag,
    CAST("Malaria, Previous 52 weeks Max†" AS BIGINT) AS malaria_previous_52_weeks_max,
    "Malaria, Previous 52 weeks Max†, flag" AS malaria_previous_52_weeks_max_flag,
    CAST("Malaria, Cum 2022†" AS BIGINT) AS malaria_cum_2022,
    "Malaria, Cum 2022†, flag" AS malaria_cum_2022_flag,
    CAST("Malaria, Cum 2021†" AS BIGINT) AS malaria_cum_2021,
    "Malaria, Cum 2021†, flag" AS malaria_cum_2021_flag,
    "Measles§, Imported, Current week" AS measles_imported_current_week,
    "Measles§, Imported, Current week, flag" AS measles_imported_current_week_flag,
    CAST("Measles§, Imported, Previous 52 weeks Max†" AS BIGINT) AS measles_imported_previous_52_weeks_max,
    "Measles§, Imported, Previous 52 weeks Max†, flag" AS measles_imported_previous_52_weeks_max_flag,
    "Measles§, Imported, Cum 2022†" AS measles_imported_cum_2022,
    "Measles§, Imported, Cum 2022†, flag" AS measles_imported_cum_2022_flag,
    "Measles§, Imported, Cum 2021†" AS measles_imported_cum_2021,
    "Measles§, Imported, Cum 2021†, flag" AS measles_imported_cum_2021_flag,
    "Measles§, Indigenous, Current week" AS measles_indigenous_current_week,
    "Measles§, Indigenous, Current week, flag" AS measles_indigenous_current_week_flag,
    CAST("Measles§, Indigenous, Previous 52 weeks Max†" AS BIGINT) AS measles_indigenous_previous_52_weeks_max,
    "Measles§, Indigenous, Previous 52 weeks Max†, flag" AS measles_indigenous_previous_52_weeks_max_flag,
    "Measles§, Indigenous, Cum 2022†" AS measles_indigenous_cum_2022,
    "Measles§, Indigenous, Cum 2022†, flag" AS measles_indigenous_cum_2022_flag,
    "Measles§, Indigenous, Cum 2021†" AS measles_indigenous_cum_2021,
    "Measles§, Indigenous, Cum 2021†, flag" AS measles_indigenous_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-kpbd-vsd5"
