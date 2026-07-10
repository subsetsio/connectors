-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Non-b serotype, Current week" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_non_b_serotype_current_week,
    "Haemophilus influenza, invasive disease, Age <5 years, Non-b serotype, Current week, flag" AS haemophilus_influenza_invasive_disease_age_5_years_non_b_serotype_current_week_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Non-b serotype, Previous 52 weeks Max†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_non_b_serotype_previous_52_weeks_max,
    "Haemophilus influenza, invasive disease, Age <5 years, Non-b serotype, Previous 52 weeks Max†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_non_b_serotype_previous_52_weeks_max_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Non-b serotype, Cum 2022†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_non_b_serotype_cum_2022,
    "Haemophilus influenza, invasive disease, Age <5 years, Non-b serotype, Cum 2022†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_non_b_serotype_cum_2022_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Non-b serotype, Cum 2021†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_non_b_serotype_cum_2021,
    "Haemophilus influenza, invasive disease, Age <5 years, Non-b serotype, Cum 2021†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_non_b_serotype_cum_2021_flag,
    "Haemophilus influenza, invasive disease, Age <5 years, Nontypeable, Current week" AS haemophilus_influenza_invasive_disease_age_5_years_nontypeable_current_week,
    "Haemophilus influenza, invasive disease, Age <5 years, Nontypeable, Current week, flag" AS haemophilus_influenza_invasive_disease_age_5_years_nontypeable_current_week_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Nontypeable, Previous 52 weeks Max†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_nontypeable_previous_52_weeks_max,
    "Haemophilus influenza, invasive disease, Age <5 years, Nontypeable, Previous 52 weeks Max†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_nontypeable_previous_52_weeks_max_flag,
    "Haemophilus influenza, invasive disease, Age <5 years, Nontypeable, Cum 2022†" AS haemophilus_influenza_invasive_disease_age_5_years_nontypeable_cum_2022,
    "Haemophilus influenza, invasive disease, Age <5 years, Nontypeable, Cum 2022†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_nontypeable_cum_2022_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Nontypeable, Cum 2021†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_nontypeable_cum_2021,
    "Haemophilus influenza, invasive disease, Age <5 years, Nontypeable, Cum 2021†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_nontypeable_cum_2021_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Unknown serotype, Current week" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_unknown_serotype_current_week,
    "Haemophilus influenza, invasive disease, Age <5 years, Unknown serotype, Current week, flag" AS haemophilus_influenza_invasive_disease_age_5_years_unknown_serotype_current_week_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Unknown serotype, Previous 52 weeks Max†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_unknown_serotype_previous_52_weeks_max,
    "Haemophilus influenza, invasive disease, Age <5 years, Unknown serotype, Previous 52 weeks Max†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_unknown_serotype_previous_52_weeks_max_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Unknown serotype, Cum 2022†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_unknown_serotype_cum_2022,
    "Haemophilus influenza, invasive disease, Age <5 years, Unknown serotype, Cum 2022†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_unknown_serotype_cum_2022_flag,
    CAST("Haemophilus influenza, invasive disease, Age <5 years, Unknown serotype, Cum 2021†" AS BIGINT) AS haemophilus_influenza_invasive_disease_age_5_years_unknown_serotype_cum_2021,
    "Haemophilus influenza, invasive disease, Age <5 years, Unknown serotype, Cum 2021†, flag" AS haemophilus_influenza_invasive_disease_age_5_years_unknown_serotype_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-g6fu-zp23"
