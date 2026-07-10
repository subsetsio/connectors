-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Tetanus, Current week" AS tetanus_current_week,
    "Tetanus, Current week, flag" AS tetanus_current_week_flag,
    CAST("Tetanus, Previous 52 weeks Max†" AS BIGINT) AS tetanus_previous_52_weeks_max,
    "Tetanus, Previous 52 weeks Max†, flag" AS tetanus_previous_52_weeks_max_flag,
    "Tetanus, Cum 2022†" AS tetanus_cum_2022,
    "Tetanus, Cum 2022†, flag" AS tetanus_cum_2022_flag,
    CAST("Tetanus, Cum 2021†" AS BIGINT) AS tetanus_cum_2021,
    "Tetanus, Cum 2021†, flag" AS tetanus_cum_2021_flag,
    "Toxic shock snydrome (other than Streptococcal), Current week" AS toxic_shock_snydrome_other_than_streptococcal_current_week,
    "Toxic shock snydrome (other than Streptococcal), Current week, flag" AS toxic_shock_snydrome_other_than_streptococcal_current_week_flag,
    CAST("Toxic shock snydrome (other than Streptococcal), Previous 52 weeks Max†" AS BIGINT) AS toxic_shock_snydrome_other_than_streptococcal_previous_52_weeks_max,
    "Toxic shock snydrome (other than Streptococcal), Previous 52 weeks Max†, flag" AS toxic_shock_snydrome_other_than_streptococcal_previous_52_weeks_max_flag,
    "Toxic shock snydrome (other than Streptococcal), Cum 2022†" AS toxic_shock_snydrome_other_than_streptococcal_cum_2022,
    "Toxic shock snydrome (other than Streptococcal), Cum 2022†, flag" AS toxic_shock_snydrome_other_than_streptococcal_cum_2022_flag,
    CAST("Toxic shock snydrome (other than Streptococcal), Cum 2021†" AS BIGINT) AS toxic_shock_snydrome_other_than_streptococcal_cum_2021,
    "Toxic shock snydrome (other than Streptococcal), Cum 2021†, flag" AS toxic_shock_snydrome_other_than_streptococcal_cum_2021_flag,
    "Trichinellosis, Current week" AS trichinellosis_current_week,
    "Trichinellosis, Current week, flag" AS trichinellosis_current_week_flag,
    CAST("Trichinellosis, Previous 52 weeks Max†" AS BIGINT) AS trichinellosis_previous_52_weeks_max,
    "Trichinellosis, Previous 52 weeks Max†, flag" AS trichinellosis_previous_52_weeks_max_flag,
    "Trichinellosis, Cum 2022†" AS trichinellosis_cum_2022,
    "Trichinellosis, Cum 2022†, flag" AS trichinellosis_cum_2022_flag,
    "Trichinellosis, Cum 2021†" AS trichinellosis_cum_2021,
    "Trichinellosis, Cum 2021†, flag" AS trichinellosis_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-hyak-nxqs"
