-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Tetanus, Current week" AS BIGINT) AS tetanus_current_week,
    "Tetanus, Current week, flag" AS tetanus_current_week_flag,
    CAST("Tetanus, Previous 52 weeks Max†" AS BIGINT) AS tetanus_previous_52_weeks_max,
    "Tetanus, Previous 52 weeks Max†, flag" AS tetanus_previous_52_weeks_max_flag,
    CAST("Tetanus, Cum 2021†" AS BIGINT) AS tetanus_cum_2021,
    "Tetanus, Cum 2021†, flag" AS tetanus_cum_2021_flag,
    CAST("Tetanus, Cum 2020†" AS BIGINT) AS tetanus_cum_2020,
    "Tetanus, Cum 2020†, flag" AS tetanus_cum_2020_flag,
    "Toxic shock snydrome (other than Streptococcal), Current week" AS toxic_shock_snydrome_other_than_streptococcal_current_week,
    "Toxic shock snydrome (other than Streptococcal), Current week, flag" AS toxic_shock_snydrome_other_than_streptococcal_current_week_flag,
    CAST("Toxic shock snydrome (other than Streptococcal), Previous 52 weeks Max†" AS BIGINT) AS toxic_shock_snydrome_other_than_streptococcal_previous_52_weeks_max,
    "Toxic shock snydrome (other than Streptococcal), Previous 52 weeks Max†, flag" AS toxic_shock_snydrome_other_than_streptococcal_previous_52_weeks_max_flag,
    CAST("Toxic shock snydrome (other than Streptococcal), Cum 2021†" AS BIGINT) AS toxic_shock_snydrome_other_than_streptococcal_cum_2021,
    "Toxic shock snydrome (other than Streptococcal), Cum 2021†, flag" AS toxic_shock_snydrome_other_than_streptococcal_cum_2021_flag,
    CAST("Toxic shock snydrome (other than Streptococcal), Cum 2020†" AS BIGINT) AS toxic_shock_snydrome_other_than_streptococcal_cum_2020,
    "Toxic shock snydrome (other than Streptococcal), Cum 2020†, flag" AS toxic_shock_snydrome_other_than_streptococcal_cum_2020_flag,
    CAST("Trichinellosis, Current week" AS BIGINT) AS trichinellosis_current_week,
    "Trichinellosis, Current week, flag" AS trichinellosis_current_week_flag,
    CAST("Trichinellosis, Previous 52 weeks Max†" AS BIGINT) AS trichinellosis_previous_52_weeks_max,
    "Trichinellosis, Previous 52 weeks Max†, flag" AS trichinellosis_previous_52_weeks_max_flag,
    CAST("Trichinellosis, Cum 2021†" AS BIGINT) AS trichinellosis_cum_2021,
    "Trichinellosis, Cum 2021†, flag" AS trichinellosis_cum_2021_flag,
    CAST("Trichinellosis, Cum 2020†" AS BIGINT) AS trichinellosis_cum_2020,
    "Trichinellosis, Cum 2020†, flag" AS trichinellosis_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-9x7v-wy9u"
