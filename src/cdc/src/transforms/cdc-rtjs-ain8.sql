-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Vancomycin-intermediate Staphylococcus aureus, Current week" AS BIGINT) AS vancomycin_intermediate_staphylococcus_aureus_current_week,
    "Vancomycin-intermediate Staphylococcus aureus, Current week, flag" AS vancomycin_intermediate_staphylococcus_aureus_current_week_flag,
    CAST("Vancomycin-intermediate Staphylococcus aureus, Previous 52 weeks Max†" AS BIGINT) AS vancomycin_intermediate_staphylococcus_aureus_previous_52_weeks_max,
    "Vancomycin-intermediate Staphylococcus aureus, Previous 52 weeks Max†, flag" AS vancomycin_intermediate_staphylococcus_aureus_previous_52_weeks_max_flag,
    CAST("Vancomycin-intermediate Staphylococcus aureus, Cum 2021†" AS BIGINT) AS vancomycin_intermediate_staphylococcus_aureus_cum_2021,
    "Vancomycin-intermediate Staphylococcus aureus, Cum 2021†, flag" AS vancomycin_intermediate_staphylococcus_aureus_cum_2021_flag,
    CAST("Vancomycin-intermediate Staphylococcus aureus, Cum 2020†" AS BIGINT) AS vancomycin_intermediate_staphylococcus_aureus_cum_2020,
    "Vancomycin-intermediate Staphylococcus aureus, Cum 2020†, flag" AS vancomycin_intermediate_staphylococcus_aureus_cum_2020_flag,
    "Vancomycin-resistant Staphylococcus aureus, Current week" AS vancomycin_resistant_staphylococcus_aureus_current_week,
    "Vancomycin-resistant Staphylococcus aureus, Current week, flag" AS vancomycin_resistant_staphylococcus_aureus_current_week_flag,
    CAST("Vancomycin-resistant Staphylococcus aureus, Previous 52 weeks Max†" AS BIGINT) AS vancomycin_resistant_staphylococcus_aureus_previous_52_weeks_max,
    "Vancomycin-resistant Staphylococcus aureus, Previous 52 weeks Max†, flag" AS vancomycin_resistant_staphylococcus_aureus_previous_52_weeks_max_flag,
    CAST("Vancomycin-resistant Staphylococcus aureus, Cum 2021†" AS BIGINT) AS vancomycin_resistant_staphylococcus_aureus_cum_2021,
    "Vancomycin-resistant Staphylococcus aureus, Cum 2021†, flag" AS vancomycin_resistant_staphylococcus_aureus_cum_2021_flag,
    CAST("Vancomycin-resistant Staphylococcus aureus, Cum 2020†" AS BIGINT) AS vancomycin_resistant_staphylococcus_aureus_cum_2020,
    "Vancomycin-resistant Staphylococcus aureus, Cum 2020†, flag" AS vancomycin_resistant_staphylococcus_aureus_cum_2020_flag,
    CAST("Varicella morbidity, Current week" AS BIGINT) AS varicella_morbidity_current_week,
    "Varicella morbidity, Current week, flag" AS varicella_morbidity_current_week_flag,
    CAST("Varicella morbidity, Previous 52 weeks Max†" AS BIGINT) AS varicella_morbidity_previous_52_weeks_max,
    "Varicella morbidity, Previous 52 weeks Max†, flag" AS varicella_morbidity_previous_52_weeks_max_flag,
    CAST("Varicella morbidity, Cum 2021†" AS BIGINT) AS varicella_morbidity_cum_2021,
    "Varicella morbidity, Cum 2021†, flag" AS varicella_morbidity_cum_2021_flag,
    CAST("Varicella morbidity, Cum 2020†" AS BIGINT) AS varicella_morbidity_cum_2020,
    "Varicella morbidity, Cum 2020†, flag" AS varicella_morbidity_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-rtjs-ain8"
