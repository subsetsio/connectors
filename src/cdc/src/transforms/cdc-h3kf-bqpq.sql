-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Carbapenemase-producing Carbapenem-resistant enterobacteriaceae, Current week" AS BIGINT) AS carbapenemase_producing_carbapenem_resistant_enterobacteriaceae_current_week,
    "Carbapenemase-producing Carbapenem-resistant enterobacteriaceae, Current week, flag" AS carbapenemase_producing_carbapenem_resistant_enterobacteriaceae_current_week_flag,
    CAST("Carbapenemase-producing Carbapenem-resistant enterobacteriaceae, Previous 52 weeks Max†" AS BIGINT) AS carbapenemase_producing_carbapenem_resistant_enterobacteriaceae_previous_52_weeks_max,
    "Carbapenemase-producing Carbapenem-resistant enterobacteriaceae, Previous 52 weeks Max†, flag" AS carbapenemase_producing_carbapenem_resistant_enterobacteriaceae_previous_52_weeks_max_flag,
    CAST("Carbapenemase-producing Carbapenem-resistant enterobacteriaceae, Cum 2022†" AS BIGINT) AS carbapenemase_producing_carbapenem_resistant_enterobacteriaceae_cum_2022,
    "Carbapenemase-producing Carbapenem-resistant enterobacteriaceae, Cum 2022†, flag" AS carbapenemase_producing_carbapenem_resistant_enterobacteriaceae_cum_2022_flag,
    CAST("Carbapenemase-producing Carbapenem-resistant enterobacteriaceae, Cum 2021†" AS BIGINT) AS carbapenemase_producing_carbapenem_resistant_enterobacteriaceae_cum_2021,
    "Carbapenemase-producing Carbapenem-resistant enterobacteriaceae, Cum 2021†, flag" AS carbapenemase_producing_carbapenem_resistant_enterobacteriaceae_cum_2021_flag,
    "Chancroid, Current week" AS chancroid_current_week,
    "Chancroid, Current week, flag" AS chancroid_current_week_flag,
    CAST("Chancroid, Previous 52 weeks Max†" AS BIGINT) AS chancroid_previous_52_weeks_max,
    "Chancroid, Previous 52 weeks Max†, flag" AS chancroid_previous_52_weeks_max_flag,
    "Chancroid, Cum 2022†" AS chancroid_cum_2022,
    "Chancroid, Cum 2022†, flag" AS chancroid_cum_2022_flag,
    CAST("Chancroid, Cum 2021†" AS BIGINT) AS chancroid_cum_2021,
    "Chancroid, Cum 2021†, flag" AS chancroid_cum_2021_flag,
    CAST("Chlamydia trachomatis infection§, Current week" AS BIGINT) AS chlamydia_trachomatis_infection_current_week,
    "Chlamydia trachomatis infection§, Current week, flag" AS chlamydia_trachomatis_infection_current_week_flag,
    "Chlamydia trachomatis infection§, Previous 52 weeks Max†" AS chlamydia_trachomatis_infection_previous_52_weeks_max,
    "Chlamydia trachomatis infection§, Previous 52 weeks Max†, flag" AS chlamydia_trachomatis_infection_previous_52_weeks_max_flag,
    CAST("Chlamydia trachomatis infection§, Cum 2022†" AS BIGINT) AS chlamydia_trachomatis_infection_cum_2022,
    "Chlamydia trachomatis infection§, Cum 2022†, flag" AS chlamydia_trachomatis_infection_cum_2022_flag,
    CAST("Chlamydia trachomatis infection§, Cum 2021†" AS BIGINT) AS chlamydia_trachomatis_infection_cum_2021,
    "Chlamydia trachomatis infection§, Cum 2021†, flag" AS chlamydia_trachomatis_infection_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocoding"
FROM "cdc-h3kf-bqpq"
