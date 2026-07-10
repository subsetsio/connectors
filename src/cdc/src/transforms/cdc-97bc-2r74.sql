-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Gonorrhea, Current week" AS BIGINT) AS gonorrhea_current_week,
    "Gonorrhea, Current week, flag" AS gonorrhea_current_week_flag,
    CAST("Gonorrhea, Previous 52 weeks Max†" AS BIGINT) AS gonorrhea_previous_52_weeks_max,
    "Gonorrhea, Previous 52 weeks Max†, flag" AS gonorrhea_previous_52_weeks_max_flag,
    CAST("Gonorrhea, Cum 2022†" AS BIGINT) AS gonorrhea_cum_2022,
    "Gonorrhea, Cum 2022†, flag" AS gonorrhea_cum_2022_flag,
    CAST("Gonorrhea, Cum 2021†" AS BIGINT) AS gonorrhea_cum_2021,
    "Gonorrhea, Cum 2021†, flag" AS gonorrhea_cum_2021_flag,
    CAST("Haemophilus influenza, invasive disease, All ages, all serotypes, Current week" AS BIGINT) AS haemophilus_influenza_invasive_disease_all_ages_all_serotypes_current_week,
    "Haemophilus influenza, invasive disease, All ages, all serotypes, Current week, flag" AS haemophilus_influenza_invasive_disease_all_ages_all_serotypes_current_week_flag,
    CAST("Haemophilus influenza, invasive disease, All ages, all serotypes, Previous 52 weeks Max†" AS BIGINT) AS haemophilus_influenza_invasive_disease_all_ages_all_serotypes_previous_52_weeks_max,
    "Haemophilus influenza, invasive disease, All ages, all serotypes, Previous 52 weeks Max†, flag" AS haemophilus_influenza_invasive_disease_all_ages_all_serotypes_previous_52_weeks_max_flag,
    CAST("Haemophilus influenza, invasive disease, All ages, all serotypes, Cum 2022†" AS BIGINT) AS haemophilus_influenza_invasive_disease_all_ages_all_serotypes_cum_2022,
    "Haemophilus influenza, invasive disease, All ages, all serotypes, Cum 2022†, flag" AS haemophilus_influenza_invasive_disease_all_ages_all_serotypes_cum_2022_flag,
    CAST("Haemophilus influenza, invasive disease, All ages, all serotypes, Cum 2021†" AS BIGINT) AS haemophilus_influenza_invasive_disease_all_ages_all_serotypes_cum_2021,
    "Haemophilus influenza, invasive disease, All ages, all serotypes, Cum 2021†, flag" AS haemophilus_influenza_invasive_disease_all_ages_all_serotypes_cum_2021_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Serotype b, Current week" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_serotype_b_current_week,
    "Haemophilus influenza, invasive disease, Age <5 years, Serotype b, Current week, flag" AS haemophilus_influenza_invasive_disease_age_5_years_serotype_b_current_week_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Serotype b, Previous 52 weeks Max†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_serotype_b_previous_52_weeks_max,
    "Haemophilus influenza, invasive disease, Age <5 years, Serotype b, Previous 52 weeks Max†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_serotype_b_previous_52_weeks_max_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Serotype b, Cum 2022†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_serotype_b_cum_2022,
    "Haemophilus influenza, invasive disease, Age <5 years, Serotype b, Cum 2022†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_serotype_b_cum_2022_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Serotype b, Cum 2021†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_serotype_b_cum_2021,
    "Haemophilus influenza, invasive disease, Age <5 years, Serotype b, Cum 2021†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_serotype_b_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-97bc-2r74"
