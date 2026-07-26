-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Arboviral diseases, Western equine encephalitis virus disease, Current week" AS arbo_dis_west_equine_enceph_virus_dis_curr_wk,
    "Arboviral diseases, Western equine encephalitis virus disease, Current week, flag" AS arbo_dis_west_equine_enceph_virus_dis_curr_wk_flag,
    CAST("Arboviral diseases, Western equine encephalitis virus disease, Previous 52 weeks Max†" AS BIGINT) AS arbo_dis_west_equine_enceph_virus_dis_prev_52wk_max,
    "Arboviral diseases, Western equine encephalitis virus disease, Previous 52 weeks Max†, flag" AS arbo_dis_west_equine_enceph_virus_dis_prev_52wk_max_flag,
    "Arboviral diseases, Western equine encephalitis virus disease, Cum 2021†" AS arbo_dis_west_equine_enceph_virus_dis_cum_2021,
    "Arboviral diseases, Western equine encephalitis virus disease, Cum 2021†, flag" AS arbo_dis_west_equine_enceph_virus_dis_cum_2021_flag,
    "Arboviral diseases, Western equine encephalitis virus disease, Cum 2020†" AS arbo_dis_west_equine_enceph_virus_dis_cum_2020,
    "Arboviral diseases, Western equine encephalitis virus disease, Cum 2020†, flag" AS arbo_dis_west_equine_enceph_virus_dis_cum_2020_flag,
    CAST("Babesiosis, Current week" AS BIGINT) AS babesiosis_current_week,
    "Babesiosis, Current week, flag" AS babesiosis_current_week_flag,
    CAST("Babesiosis, Previous 52 weeks Max†" AS BIGINT) AS babesiosis_previous_52_weeks_max,
    "Babesiosis, Previous 52 weeks Max†, flag" AS babesiosis_previous_52_weeks_max_flag,
    CAST("Babesiosis, Cum 2021†" AS BIGINT) AS babesiosis_cum_2021,
    "Babesiosis, Cum 2021†, flag" AS babesiosis_cum_2021_flag,
    CAST("Babesiosis, Cum 2020†" AS BIGINT) AS babesiosis_cum_2020,
    "Babesiosis, Cum 2020†, flag" AS babesiosis_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-hkr7-mcee"
