-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Meningococcal disease, All serogroups, Current week" AS BIGINT) AS meningococcal_disease_all_serogroups_current_week,
    "Meningococcal disease, All serogroups, Current week, flag" AS meningococcal_disease_all_serogroups_current_week_flag,
    CAST("Meningococcal disease, All serogroups, Previous 52 weeks Max†" AS BIGINT) AS meningococcal_disease_all_serogroups_previous_52_weeks_max,
    "Meningococcal disease, All serogroups, Previous 52 weeks Max†, flag" AS meningococcal_disease_all_serogroups_previous_52_weeks_max_flag,
    CAST("Meningococcal disease, All serogroups, Cum 2022†" AS BIGINT) AS meningococcal_disease_all_serogroups_cum_2022,
    "Meningococcal disease, All serogroups, Cum 2022†, flag" AS meningococcal_disease_all_serogroups_cum_2022_flag,
    CAST("Meningococcal disease, All serogroups, Cum 2021†" AS BIGINT) AS meningococcal_disease_all_serogroups_cum_2021,
    "Meningococcal disease, All serogroups, Cum 2021†, flag" AS meningococcal_disease_all_serogroups_cum_2021_flag,
    "Meningococcal disease, Serogroups ACWY, Current week" AS meningococcal_disease_serogroups_acwy_current_week,
    "Meningococcal disease, Serogroups ACWY, Current week, flag" AS meningococcal_disease_serogroups_acwy_current_week_flag,
    CAST("Meningococcal disease, Serogroups ACWY, Previous 52 weeks Max†" AS BIGINT) AS meningococcal_disease_serogroups_acwy_previous_52_weeks_max,
    "Meningococcal disease, Serogroups ACWY, Previous 52 weeks Max†, flag" AS meningococcal_disease_serogroups_acwy_previous_52_weeks_max_flag,
    "Meningococcal disease, Serogroups ACWY, Cum 2022†" AS meningococcal_disease_serogroups_acwy_cum_2022,
    "Meningococcal disease, Serogroups ACWY, Cum 2022†, flag" AS meningococcal_disease_serogroups_acwy_cum_2022_flag,
    CAST("Meningococcal disease, Serogroups ACWY, Cum 2021†" AS BIGINT) AS meningococcal_disease_serogroups_acwy_cum_2021,
    "Meningococcal disease, Serogroups ACWY, Cum 2021†, flag" AS meningococcal_disease_serogroups_acwy_cum_2021_flag,
    "Meningococcal disease, Serogroup B, Current week" AS meningococcal_disease_serogroup_b_current_week,
    "Meningococcal disease, Serogroup B, Current week, flag" AS meningococcal_disease_serogroup_b_current_week_flag,
    CAST("Meningococcal disease, Serogroup B, Previous 52 weeks Max†" AS BIGINT) AS meningococcal_disease_serogroup_b_previous_52_weeks_max,
    "Meningococcal disease, Serogroup B, Previous 52 weeks Max†, flag" AS meningococcal_disease_serogroup_b_previous_52_weeks_max_flag,
    CAST("Meningococcal disease, Serogroup B, Cum 2022†" AS BIGINT) AS meningococcal_disease_serogroup_b_cum_2022,
    "Meningococcal disease, Serogroup B, Cum 2022†, flag" AS meningococcal_disease_serogroup_b_cum_2022_flag,
    CAST("Meningococcal disease, Serogroup B, Cum 2021†" AS BIGINT) AS meningococcal_disease_serogroup_b_cum_2021,
    "Meningococcal disease, Serogroup B, Cum 2021†, flag" AS meningococcal_disease_serogroup_b_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-vmgc-uspy"
