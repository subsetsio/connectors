-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Current week" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_infection_current_week,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Current week, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_infection_current_week_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Previous 52 weeks Max†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_infection_previous_52_weeks_max,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Previous 52 weeks Max†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_infection_previous_52_weeks_max_flag,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Cum 2022†" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_infection_cum_2022,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Cum 2022†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_infection_cum_2022_flag,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Cum 2021†" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_infection_cum_2021,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia ewingii infection, Cum 2021†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_ewingii_infection_cum_2021_flag,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Current week" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_anaplasmosis_current_week,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Current week, flag" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_anaplasmosis_current_week_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Previous 52 weeks Max†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_anaplasmosis_previous_52_weeks_max,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Previous 52 weeks Max†, flag" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_anaplasmosis_previous_52_weeks_max_flag,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Cum 2022†" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_anaplasmosis_cum_2022,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Cum 2022†, flag" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_anaplasmosis_cum_2022_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Cum 2021†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_anaplasmosis_cum_2021,
    "Ehrlichiosis and Anaplasmosis, Undetermined ehrlichiosis/anaplasmosis, Cum 2021†, flag" AS ehrlichiosis_and_anaplasmosis_undetermined_ehrlichiosis_anaplasmosis_cum_2021_flag,
    CAST("Giardiasis, Current week" AS BIGINT) AS giardiasis_current_week,
    "Giardiasis, Current week, flag" AS giardiasis_current_week_flag,
    CAST("Giardiasis, Previous 52 weeks Max†" AS BIGINT) AS giardiasis_previous_52_weeks_max,
    "Giardiasis, Previous 52 weeks Max†, flag" AS giardiasis_previous_52_weeks_max_flag,
    CAST("Giardiasis, Cum 2022†" AS BIGINT) AS giardiasis_cum_2022,
    "Giardiasis, Cum 2022†, flag" AS giardiasis_cum_2022_flag,
    CAST("Giardiasis, Cum 2021†" AS BIGINT) AS giardiasis_cum_2021,
    "Giardiasis, Cum 2021†, flag" AS giardiasis_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-wzwe-859x"
