-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Current week" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_dad8605b,
    "Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Current week, flag" AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_281ca1ea,
    CAST("Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Previous 52 weeks Max†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_3ee34371,
    "Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Previous 52 weeks Max†, flag" AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_5aa84456,
    CAST("Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Cum 2022†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_6667764d,
    "Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Cum 2022†, flag" AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_02ba23cc,
    CAST("Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Cum 2021†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_cbff626c,
    "Ehrlichiosis and Anaplasmosis, Anaplasma phagocytophilum infection, Cum 2021†, flag" AS ehrlichiosis_and_anaplasmosis_anaplasma_phagocytophilum_b6f6553d,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Current week" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_inf_curr_wk,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Current week, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_inf_cbd8b505,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Previous 52 weeks Max†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_inf_6c5902ed,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Previous 52 weeks Max†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_inf_0ba35282,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Cum 2022†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_inf_cum_2022,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Cum 2022†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_inf_d4627dc0,
    CAST("Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Cum 2021†" AS BIGINT) AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_inf_cum_2021,
    "Ehrlichiosis and Anaplasmosis, Ehrlichia chaffeensis infection, Cum 2021†, flag" AS ehrlichiosis_and_anaplasmosis_ehrlichia_chaffeensis_inf_90d9bdbf,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-sixg-saap"
