-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Viral hemorrhagic fevers§, Sabia virus¶, Current week" AS viral_hemorrhagic_fevers_sabia_virus_current_week,
    "Viral hemorrhagic fevers§ , Sabia virus¶, Current week, flag" AS viral_hemorrhagic_fevers_sabia_virus_current_week_flag,
    "Viral hemorrhagic fevers§, Sabia virus¶, Previous 52 weeks Max†" AS viral_hemorrhagic_fevers_sabia_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Sabia virus¶, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_sabia_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Sabia virus¶, Cum 2022†" AS viral_hemorrhagic_fevers_sabia_virus_cum_2022,
    "Viral hemorrhagic fevers§, Sabia virus¶, Cum 2022†, flag" AS viral_hemorrhagic_fevers_sabia_virus_cum_2022_flag,
    "Viral hemorrhagic fevers§, Sabia virus¶, Cum 2021†" AS viral_hemorrhagic_fevers_sabia_virus_cum_2021,
    "Viral hemorrhagic fevers§, Sabia virus¶, Cum 2021†, flag" AS viral_hemorrhagic_fevers_sabia_virus_cum_2021_flag,
    "Yellow fever, Current week" AS yellow_fever_current_week,
    "Yellow fever, Current week, flag" AS yellow_fever_current_week_flag,
    CAST("Yellow fever, Previous 52 weeks Max†" AS BIGINT) AS yellow_fever_previous_52_weeks_max,
    "Yellow fever, Previous 52 weeks Max†, flag" AS yellow_fever_previous_52_weeks_max_flag,
    "Yellow fever, Cum 2022†" AS yellow_fever_cum_2022,
    "Yellow fever, Cum 2022†, flag" AS yellow_fever_cum_2022_flag,
    "Yellow fever, Cum 2021†" AS yellow_fever_cum_2021,
    "Yellow fever, Cum 2021†, flag" AS yellow_fever_cum_2021_flag,
    "Zika virus disease, non-congenital, Current week" AS zika_virus_disease_non_congenital_current_week,
    "Zika virus disease, non-congenital, Current week, flag" AS zika_virus_disease_non_congenital_current_week_flag,
    CAST("Zika virus disease, non-congenital, Previous 52 weeks Max†" AS BIGINT) AS zika_virus_disease_non_congenital_previous_52_weeks_max,
    "Zika virus disease, non-congenital, Previous 52 weeks Max†, flag" AS zika_virus_disease_non_congenital_previous_52_weeks_max_flag,
    "Zika virus disease, non-congenital, Cum 2022†" AS zika_virus_disease_non_congenital_cum_2022,
    "Zika virus disease, non-congenital, Cum 2022†, flag" AS zika_virus_disease_non_congenital_cum_2022_flag,
    CAST("Zika virus disease, non-congenital, Cum 2021†" AS BIGINT) AS zika_virus_disease_non_congenital_cum_2021,
    "Zika virus disease, non-congenital, Cum 2021†, flag" AS zika_virus_disease_non_congenital_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-3nij-2pw6"
