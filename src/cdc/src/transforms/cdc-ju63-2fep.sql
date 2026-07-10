-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Anthrax, Current week" AS anthrax_current_week,
    "Anthrax, Current week, flag" AS anthrax_current_week_flag,
    CAST("Anthrax, Previous 52 weeks Max†" AS BIGINT) AS anthrax_previous_52_weeks_max,
    "Anthrax, Previous 52 weeks Max†, flag" AS anthrax_previous_52_weeks_max_flag,
    "Anthrax, Cum 2021†" AS anthrax_cum_2021,
    "Anthrax, Cum 2021†, flag" AS anthrax_cum_2021_flag,
    CAST("Anthrax, Cum 2020†" AS BIGINT) AS anthrax_cum_2020,
    "Anthrax, Cum 2020†, flag" AS anthrax_cum_2020_flag,
    "Arboviral diseases, Chikungunya virus disease, Current week" AS arboviral_diseases_chikungunya_virus_disease_current_week,
    "Arboviral diseases, Chikungunya virus disease, Current week, flag" AS arboviral_diseases_chikungunya_virus_disease_current_week_flag,
    CAST("Arboviral diseases, Chikungunya virus disease, Previous 52 weeks Max†" AS BIGINT) AS arboviral_diseases_chikungunya_virus_disease_previous_52_weeks_max,
    "Arboviral diseases,Chikungunya virus disease, Previous 52 weeks Max†, flag" AS arboviral_diseases_chikungunya_virus_disease_previous_52_weeks_max_flag,
    CAST("Arboviral diseases,Chikungunya virus disease, Cum 2021†" AS BIGINT) AS arboviral_diseases_chikungunya_virus_disease_cum_2021,
    "Arboviral diseases, Chikungunya virus disease, Cum 2021†, flag" AS arboviral_diseases_chikungunya_virus_disease_cum_2021_flag,
    CAST("Arboviral diseases, Chikungunya virus disease, Cum 2020†" AS BIGINT) AS arboviral_diseases_chikungunya_virus_disease_cum_2020,
    "Arboviral diseases, Chikungunya virus disease, Cum 2020†, flag" AS arboviral_diseases_chikungunya_virus_disease_cum_2020_flag,
    "Arboviral diseases, Eastern equine encephalitis virus disease, Current week" AS arboviral_diseases_eastern_equine_encephalitis_virus_disease_current_week,
    "Arboviral diseases, Eastern equine encephalitis virus disease, Current week, flag" AS arboviral_diseases_eastern_equine_encephalitis_virus_disease_current_week_flag,
    CAST("Arboviral diseases, Eastern equine encephalitis virus disease, Previous 52 weeks Max†" AS BIGINT) AS arboviral_diseases_eastern_equine_encephalitis_virus_disease_previous_52_weeks_max,
    "Arboviral diseases, Eastern equine encephalitis virus disease, Previous 52 weeks Max†, flag" AS arboviral_diseases_eastern_equine_encephalitis_virus_disease_previous_52_weeks_max_flag,
    CAST("Arboviral diseases, Eastern equine encephalitis virus disease, Cum 2021†" AS BIGINT) AS arboviral_diseases_eastern_equine_encephalitis_virus_disease_cum_2021,
    "Arboviral diseases,Eastern equine encephalitis virus disease, Cum 2021†, flag" AS arboviral_diseases_eastern_equine_encephalitis_virus_disease_cum_2021_flag,
    CAST("Arboviral diseases, Eastern equine encephalitis virus disease, Cum 2020†" AS BIGINT) AS arboviral_diseases_eastern_equine_encephalitis_virus_disease_cum_2020,
    "Arboviral diseases, Eastern equine encephalitis virus disease, Cum 2020†, flag" AS arboviral_diseases_eastern_equine_encephalitis_virus_disease_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "Geocode" AS geocode
FROM "cdc-ju63-2fep"
