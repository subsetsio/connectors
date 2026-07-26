-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Invasive pneumococcal disease, all ages§, Confirmed, Current week" AS BIGINT) AS invasive_pneumococcal_disease_all_ages_confirmed_current_week,
    "Invasive pneumococcal disease, all ages§, Confirmed, Current week, flag" AS inv_pneumococcal_dis_all_age_conf_curr_wk_flag,
    CAST("Invasive pneumococcal disease, all ages§, Confirmed, Previous 52 weeks Max†" AS BIGINT) AS inv_pneumococcal_dis_all_age_conf_prev_52wk_max,
    "Invasive pneumococcal disease, all ages§, Confirmed, Previous 52 weeks Max†, flag" AS inv_pneumococcal_dis_all_age_conf_prev_52wk_max_flag,
    CAST("Invasive pneumococcal disease, all ages§, Confirmed, Cum 2021†" AS BIGINT) AS invasive_pneumococcal_disease_all_ages_confirmed_cum_2021,
    "Invasive pneumococcal disease, all ages§, Confirmed, Cum 2021†, flag" AS invasive_pneumococcal_disease_all_ages_confirmed_cum_2021_flag,
    CAST("Invasive pneumococcal disease, all ages§, Confirmed, Cum 2020†" AS BIGINT) AS invasive_pneumococcal_disease_all_ages_confirmed_cum_2020,
    "Invasive pneumococcal disease, all ages§, Confirmed, Cum 2020†, flag" AS invasive_pneumococcal_disease_all_ages_confirmed_cum_2020_flag,
    CAST("Invasive pneumococcal disease, all ages§, Probable, Current week" AS BIGINT) AS invasive_pneumococcal_disease_all_ages_probable_current_week,
    "Invasive pneumococcal disease, all ages§, Probable, Current week, flag" AS inv_pneumococcal_dis_all_age_prob_curr_wk_flag,
    CAST("Invasive pneumococcal disease, all ages§, Probable, Previous 52 weeks Max†" AS BIGINT) AS inv_pneumococcal_dis_all_age_prob_prev_52wk_max,
    "Invasive pneumococcal disease, all ages§, Probable, Previous 52 weeks Max†, flag" AS inv_pneumococcal_dis_all_age_prob_prev_52wk_max_flag,
    CAST("Invasive pneumococcal disease, all ages§, Probable,  Cum 2021†" AS BIGINT) AS invasive_pneumococcal_disease_all_ages_probable_cum_2021,
    "Invasive pneumococcal disease, all ages§, Probable,  Cum 2021†, flag" AS invasive_pneumococcal_disease_all_ages_probable_cum_2021_flag,
    CAST("Invasive pneumococcal disease, all ages§, Probable,  Cum 2020†" AS BIGINT) AS invasive_pneumococcal_disease_all_ages_probable_cum_2020,
    "Invasive pneumococcal disease, all ages§, Probable, Cum 2020†, flag" AS invasive_pneumococcal_disease_all_ages_probable_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-mrip-2k2a"
