-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Arboviral diseases, St. Louis encephalitis virus disease, Current week" AS arboviral_diseases_st_louis_encephalitis_virus_disease_current_week,
    "Arboviral diseases, St. Louis encephalitis virus disease, Current week, flag" AS arboviral_diseases_st_louis_encephalitis_virus_disease_current_week_flag,
    CAST("Arboviral diseases, St. Louis encephalitis virus disease, Previous 52 weeks Max†" AS BIGINT) AS arboviral_diseases_st_louis_encephalitis_virus_disease_previous_52_weeks_max,
    "Arboviral diseases, St. Louis encephalitis virus disease, Previous 52 weeks Max†, flag" AS arboviral_diseases_st_louis_encephalitis_virus_disease_previous_52_weeks_max_flag,
    "Arboviral diseases, St. Louis encephalitis virus disease, Cum 2022†" AS arboviral_diseases_st_louis_encephalitis_virus_disease_cum_2022,
    "Arboviral diseases, St. Louis encephalitis virus disease, Cum 2022†, flag" AS arboviral_diseases_st_louis_encephalitis_virus_disease_cum_2022_flag,
    "Arboviral diseases, St. Louis encephalitis virus disease, Cum 2021†" AS arboviral_diseases_st_louis_encephalitis_virus_disease_cum_2021,
    "Arboviral diseases, St. Louis encephalitis virus disease, Cum 2021†, flag" AS arboviral_diseases_st_louis_encephalitis_virus_disease_cum_2021_flag,
    CAST("Arboviral diseases, West Nile virus disease, Current week" AS BIGINT) AS arboviral_diseases_west_nile_virus_disease_current_week,
    "Arboviral diseases, West Nile virus disease, Current week, flag" AS arboviral_diseases_west_nile_virus_disease_current_week_flag,
    CAST("Arboviral diseases, West Nile virus disease, Previous 52 weeks Max†" AS BIGINT) AS arboviral_diseases_west_nile_virus_disease_previous_52_weeks_max,
    "Arboviral diseases, West Nile virus disease, Previous 52 weeks Max†, flag" AS arboviral_diseases_west_nile_virus_disease_previous_52_weeks_max_flag,
    CAST("Arboviral diseases, West Nile virus disease, Cum 2022†" AS BIGINT) AS arboviral_diseases_west_nile_virus_disease_cum_2022,
    "Arboviral diseases, West Nile virus disease, Cum 2022†, flag" AS arboviral_diseases_west_nile_virus_disease_cum_2022_flag,
    CAST("Arboviral diseases, West Nile virus disease, Cum 2021†" AS BIGINT) AS arboviral_diseases_west_nile_virus_disease_cum_2021,
    "Arboviral diseases, West Nile virus disease, Cum 2021†, flag" AS arboviral_diseases_west_nile_virus_disease_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-q8j9-sue7"
