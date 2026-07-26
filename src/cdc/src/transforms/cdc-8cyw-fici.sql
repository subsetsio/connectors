-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Current week" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_inf_curr_wk,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Current week, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_inf_curr_wk_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Previous 52 weeks Max†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_inf_pre_9aee2be6,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Previous 52 weeks Max†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_inf_pre_33cfe91e,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Cum 2021†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_inf_cum_2021,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Cum 2021†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_inf_cum_aa4ff272,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Cum 2020†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_inf_cum_2020,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Cum 2020†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_inf_cum_203c8f82,
    CAST("Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Current week" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_d37d68e1,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Current week, flag" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_6b573b39,
    CAST("Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Previous 52 weeks Max†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_d165ec53,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Previous 52 weeks Max†, flag" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_fe6671fa,
    CAST("Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Cum 2021†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_51fed6ca,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Cum 2021†, flag" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_bab20862,
    CAST("Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Cum 2020†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_9f7f853c,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Cum 2020†, flag" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_0422c182,
    CAST("Giardiasis, Current week" AS BIGINT) AS giardiasis_current_week,
    "Giardiasis, Current week, flag" AS giardiasis_current_week_flag,
    CAST("Giardiasis, Previous 52 weeks Max†" AS BIGINT) AS giardiasis_previous_52_weeks_max,
    "Giardiasis, Previous 52 weeks Max†, flag" AS giardiasis_previous_52_weeks_max_flag,
    CAST("Giardiasis, Cum 2021†" AS BIGINT) AS giardiasis_cum_2021,
    "Giardiasis, Cum 2021†, flag" AS giardiasis_cum_2021_flag,
    CAST("Giardiasis, Cum 2020†" AS BIGINT) AS giardiasis_cum_2020,
    "Giardiasis, Cum 2020†, flag" AS giardiasis_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-8cyw-fici"
