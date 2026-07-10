-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Meningococcal disease, Other serogroups, Current week" AS meningococcal_disease_other_serogroups_current_week,
    "Meningococcal disease, Other serogroups, Current week, flag" AS meningococcal_disease_other_serogroups_current_week_flag,
    CAST("Meningococcal disease, Other serogroups, Previous 52 weeks Max†" AS BIGINT) AS meningococcal_disease_other_serogroups_previous_52_weeks_max,
    "Meningococcal disease, Other serogroups, Previous 52 weeks Max†, flag" AS meningococcal_disease_other_serogroups_previous_52_weeks_max_flag,
    CAST("Meningococcal disease, Other serogroups, Cum 2021†" AS BIGINT) AS meningococcal_disease_other_serogroups_cum_2021,
    "Meningococcal disease, Other serogroups, Cum 2021†, flag" AS meningococcal_disease_other_serogroups_cum_2021_flag,
    CAST("Meningococcal disease, Other serogroups, Cum 2020†" AS BIGINT) AS meningococcal_disease_other_serogroups_cum_2020,
    "Meningococcal disease, Other serogroups, Cum 2020†, flag" AS meningococcal_disease_other_serogroups_cum_2020_flag,
    CAST("Meningococcal disease, Unknown serogroup, Current week" AS BIGINT) AS meningococcal_disease_unknown_serogroup_current_week,
    "Meningococcal disease, Unknown serogroup, Current week, flag" AS meningococcal_disease_unknown_serogroup_current_week_flag,
    CAST("Meningococcal disease, Unknown serogroup, Previous 52 weeks Max†" AS BIGINT) AS meningococcal_disease_unknown_serogroup_previous_52_weeks_max,
    "Meningococcal disease, Unknown serogroup, Previous 52 weeks Max†, flag" AS meningococcal_disease_unknown_serogroup_previous_52_weeks_max_flag,
    CAST("Meningococcal disease, Unknown serogroup, Cum 2021†" AS BIGINT) AS meningococcal_disease_unknown_serogroup_cum_2021,
    "Meningococcal disease, Unknown serogroup, Cum 2021†, flag" AS meningococcal_disease_unknown_serogroup_cum_2021_flag,
    CAST("Meningococcal disease, Unknown serogroup, Cum 2020†" AS BIGINT) AS meningococcal_disease_unknown_serogroup_cum_2020,
    "Meningococcal disease, Unknown serogroup, Cum 2020†, flag" AS meningococcal_disease_unknown_serogroup_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-jr4g-zdpg"
