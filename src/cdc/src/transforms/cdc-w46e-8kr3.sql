-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Arboviral diseases, Jamestown Canyon virus disease, Current week" AS arboviral_diseases_jamestown_canyon_virus_disease_current_week,
    "Arboviral diseases, Jamestown Canyon virus disease, Current week, flag" AS arboviral_diseases_jamestown_canyon_virus_disease_current_week_flag,
    CAST("Arboviral diseases, Jamestown Canyon virus disease, Previous 52 weeks Max†" AS BIGINT) AS arboviral_diseases_jamestown_canyon_virus_disease_previous_52_weeks_max,
    "Arboviral diseases, Jamestown Canyon virus disease, Previous 52 weeks Max†, flag" AS arboviral_diseases_jamestown_canyon_virus_disease_previous_52_weeks_max_flag,
    CAST("Arboviral diseases, Jamestown Canyon virus disease, Cum 2021†" AS BIGINT) AS arboviral_diseases_jamestown_canyon_virus_disease_cum_2021,
    "Arboviral diseases, Jamestown Canyon virus disease, Cum 2021†, flag" AS arboviral_diseases_jamestown_canyon_virus_disease_cum_2021_flag,
    CAST("Arboviral diseases, Jamestown Canyon virus disease, Cum 2020†" AS BIGINT) AS arboviral_diseases_jamestown_canyon_virus_disease_cum_2020,
    "Arboviral diseases, Jamestown Canyon virus disease, Cum 2020†, flag" AS arboviral_diseases_jamestown_canyon_virus_disease_cum_2020_flag,
    CAST("Arboviral diseases,La Crosse virus disease, Current week" AS BIGINT) AS arboviral_diseases_la_crosse_virus_disease_current_week,
    "Arboviral diseases, La Crosse virus disease, Current week, flag" AS arboviral_diseases_la_crosse_virus_disease_current_week_flag,
    CAST("Arboviral diseases, La Crosse virus disease, Previous 52 weeks Max†" AS BIGINT) AS arboviral_diseases_la_crosse_virus_disease_previous_52_weeks_max,
    "Arboviral diseases, La Crosse virus disease, Previous 52 weeks Max†, flag" AS arboviral_diseases_la_crosse_virus_disease_previous_52_weeks_max_flag,
    CAST("Arboviral diseases, La Crosse virus disease, Cum 2021†" AS BIGINT) AS arboviral_diseases_la_crosse_virus_disease_cum_2021,
    "Arboviral diseases, La Crosse virus disease, Cum 2021†, flag" AS arboviral_diseases_la_crosse_virus_disease_cum_2021_flag,
    CAST("Arboviral diseases, La Crosse virus disease, Cum 2020†" AS BIGINT) AS arboviral_diseases_la_crosse_virus_disease_cum_2020,
    "Arboviral diseases, La Crosse virus disease, Cum 2020†, flag" AS arboviral_diseases_la_crosse_virus_disease_cum_2020_flag,
    CAST("Arboviral diseases, Powassan virus disease, Current week" AS BIGINT) AS arboviral_diseases_powassan_virus_disease_current_week,
    "Arboviral diseases, Powassan virus disease, Current week, flag" AS arboviral_diseases_powassan_virus_disease_current_week_flag,
    CAST("Arboviral diseases, Powassan virus disease, Previous 52 weeks Max†" AS BIGINT) AS arboviral_diseases_powassan_virus_disease_previous_52_weeks_max,
    "Arboviral diseases, Powassan virus disease, Previous 52 weeks Max†, flag" AS arboviral_diseases_powassan_virus_disease_previous_52_weeks_max_flag,
    CAST("Arboviral diseases, Powassan virus disease, Cum 2021†" AS BIGINT) AS arboviral_diseases_powassan_virus_disease_cum_2021,
    "Arboviral diseases, Powassan virus disease, Cum 2021†, flag" AS arboviral_diseases_powassan_virus_disease_cum_2021_flag,
    CAST("Arboviral diseases, Powassan virus disease, Cum 2020†" AS BIGINT) AS arboviral_diseases_powassan_virus_disease_cum_2020,
    "Arboviral diseases, Powassan virus disease, Cum 2020†, flag" AS arboviral_diseases_powassan_virus_disease_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "Geocode" AS geocode
FROM "cdc-w46e-8kr3"
