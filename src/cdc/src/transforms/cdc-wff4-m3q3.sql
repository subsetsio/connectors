-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Invasive pneumococcal disease, age < 5 years§, Confirmed, Current week" AS BIGINT) AS invasive_pneumococcal_disease_age_5_years_confirmed_current_week,
    "Invasive pneumococcal disease, age < 5 years§, Confirmed, Current week, flag" AS invasive_pneumococcal_disease_age_5_years_confirmed_current_week_flag,
    CAST("Invasive pneumococcal disease, age < 5 years§, Confirmed, Previous 52 weeks Max†" AS BIGINT) AS invasive_pneumococcal_disease_age_5_years_confirmed_previous_52_weeks_max,
    "Invasive pneumococcal disease, age < 5 years§, Confirmed, Previous 52 weeks Max†, flag" AS invasive_pneumococcal_disease_age_5_years_confirmed_previous_52_weeks_max_flag,
    CAST("Invasive pneumococcal disease, age < 5 years§, Confirmed, Cum 2021†" AS BIGINT) AS invasive_pneumococcal_disease_age_5_years_confirmed_cum_2021,
    "Invasive pneumococcal disease, age < 5 years§, Confirmed, Cum 2021†, flag" AS invasive_pneumococcal_disease_age_5_years_confirmed_cum_2021_flag,
    CAST("Invasive pneumococcal disease, age < 5 years§, Confirmed, Cum 2020†" AS BIGINT) AS invasive_pneumococcal_disease_age_5_years_confirmed_cum_2020,
    "Invasive pneumococcal disease, age < 5 years§, Confirmed, Cum 2020†, flag" AS invasive_pneumococcal_disease_age_5_years_confirmed_cum_2020_flag,
    CAST("Invasive pneumococcal disease, age < 5 years§, Probable, Current week" AS BIGINT) AS invasive_pneumococcal_disease_age_5_years_probable_current_week,
    "Invasive pneumococcal disease, age < 5 years§, Probable, Current week, flag" AS invasive_pneumococcal_disease_age_5_years_probable_current_week_flag,
    CAST("Invasive pneumococcal disease, age < 5 years§, Probable, Previous 52 weeks Max†" AS BIGINT) AS invasive_pneumococcal_disease_age_5_years_probable_previous_52_weeks_max,
    "Invasive pneumococcal disease, age < 5 years§, Probable, Previous 52 weeks Max†, flag" AS invasive_pneumococcal_disease_age_5_years_probable_previous_52_weeks_max_flag,
    CAST("Invasive pneumococcal disease, age < 5 years§, Probable,  Cum 2021†" AS BIGINT) AS invasive_pneumococcal_disease_age_5_years_probable_cum_2021,
    "Invasive pneumococcal disease, age < 5 years§, Probable,  Cum 2021†, flag" AS invasive_pneumococcal_disease_age_5_years_probable_cum_2021_flag,
    CAST("Invasive pneumococcal disease, age < 5 years§, Probable,  Cum 2020†" AS BIGINT) AS invasive_pneumococcal_disease_age_5_years_probable_cum_2020,
    "Invasive pneumococcal disease, age < 5 years§, Probable, Cum 2020†, flag" AS invasive_pneumococcal_disease_age_5_years_probable_cum_2020_flag,
    CAST("Legionellosis, Current week" AS BIGINT) AS legionellosis_current_week,
    "Legionellosis, Current week, flag" AS legionellosis_current_week_flag,
    CAST("Legionellosis, Previous 52 weeks Max†" AS BIGINT) AS legionellosis_previous_52_weeks_max,
    "Legionellosis, Previous 52 weeks Max†, flag" AS legionellosis_previous_52_weeks_max_flag,
    CAST("Legionellosis, Cum 2021†" AS BIGINT) AS legionellosis_cum_2021,
    "Legionellosis, Cum 2021†, flag" AS legionellosis_cum_2021_flag,
    CAST("Legionellosis, Cum 2020†" AS BIGINT) AS legionellosis_cum_2020,
    "Legionellosis, Cum 2020†, flag" AS legionellosis_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-wff4-m3q3"
