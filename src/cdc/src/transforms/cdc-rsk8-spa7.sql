-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Yellow fever, Current week" AS yellow_fever_current_week,
    "Yellow fever, Current week, flag" AS yellow_fever_current_week_flag,
    CAST("Yellow fever, Previous 52 weeks Max†" AS BIGINT) AS yellow_fever_previous_52_weeks_max,
    "Yellow fever, Previous 52 weeks Max†, flag" AS yellow_fever_previous_52_weeks_max_flag,
    "Yellow fever, Cum 2021†" AS yellow_fever_cum_2021,
    "Yellow fever, Cum 2021†, flag" AS yellow_fever_cum_2021_flag,
    "Yellow fever, Cum 2020†" AS yellow_fever_cum_2020,
    "Yellow fever, Cum 2020†, flag" AS yellow_fever_cum_2020_flag,
    CAST("Zika virus disease, non-congenital, Current week" AS BIGINT) AS zika_virus_disease_non_congenital_current_week,
    "Zika virus disease, non-congenital, Current week, flag" AS zika_virus_disease_non_congenital_current_week_flag,
    CAST("Zika virus disease, non-congenital, Previous 52 weeks Max†" AS BIGINT) AS zika_virus_disease_non_congenital_previous_52_weeks_max,
    "Zika virus disease, non-congenital, Previous 52 weeks Max†, flag" AS zika_virus_disease_non_congenital_previous_52_weeks_max_flag,
    CAST("Zika virus disease, non-congenital, Cum 2021†" AS BIGINT) AS zika_virus_disease_non_congenital_cum_2021,
    "Zika virus disease, non-congenital, Cum 2021†, flag" AS zika_virus_disease_non_congenital_cum_2021_flag,
    CAST("Zika virus disease, non-congenital, Cum 2020†" AS BIGINT) AS zika_virus_disease_non_congenital_cum_2020,
    "Zika virus disease, non-congenital, Cum 2020†, flag" AS zika_virus_disease_non_congenital_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-rsk8-spa7"
