-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Current week" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_infection_current_week,
    "Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Current week, flag" AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_infection_current_week_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Previous 52 weeks Max†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_infection_previous_52_weeks_max,
    "Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Previous 52 weeks Max†, flag" AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_infection_previous_52_weeks_max_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Cum 2021†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_infection_cum_2021,
    "Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Cum 2021†, flag" AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_infection_cum_2021_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Cum 2020†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_infection_cum_2020,
    "Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Cum 2020†, flag" AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_infection_cum_2020_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Current week" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_infection_current_week,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Current week, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_infection_current_week_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Previous 52 weeks Max†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_infection_previous_52_weeks_max,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Previous 52 weeks Max†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_infection_previous_52_weeks_max_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Cum 2021†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_infection_cum_2021,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Cum 2021†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_infection_cum_2021_flag,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Cum 2020†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_infection_cum_2020,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Cum 2020†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_infection_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-9d9z-vf8f"
