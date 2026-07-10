-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Dengue virus infections, Dengue, Current week" AS BIGINT) AS dengue_virus_infections_dengue_current_week,
    "Dengue virus infections, Dengue, Current week, flag" AS dengue_virus_infections_dengue_current_week_flag,
    CAST("Dengue virus infections, Dengue, Previous 52 weeks Max†" AS BIGINT) AS dengue_virus_infections_dengue_previous_52_weeks_max,
    "Dengue virus infections, Dengue, Previous 52 weeks Max†, flag" AS dengue_virus_infections_dengue_previous_52_weeks_max_flag,
    CAST("Dengue virus infections, Dengue, Cum 2021†" AS BIGINT) AS dengue_virus_infections_dengue_cum_2021,
    "Dengue virus infections, Dengue, Cum 2021†, flag" AS dengue_virus_infections_dengue_cum_2021_flag,
    CAST("Dengue virus infections, Dengue, Cum 2020†" AS BIGINT) AS dengue_virus_infections_dengue_cum_2020,
    "Dengue virus infections, Dengue, Cum 2020†, flag" AS dengue_virus_infections_dengue_cum_2020_flag,
    "Dengue virus infections, Dengue-like illness, Current week" AS dengue_virus_infections_dengue_like_illness_current_week,
    "Dengue virus infections, Dengue-like illness, Current week, flag" AS dengue_virus_infections_dengue_like_illness_current_week_flag,
    CAST("Dengue virus infections, Dengue-like illness, Previous 52 weeks Max†" AS BIGINT) AS dengue_virus_infections_dengue_like_illness_previous_52_weeks_max,
    "Dengue virus infections, Dengue-like illness, Previous 52 weeks Max†, flag" AS dengue_virus_infections_dengue_like_illness_previous_52_weeks_max_flag,
    CAST("Dengue virus infections, Dengue-like illness, Cum 2021†" AS BIGINT) AS dengue_virus_infections_dengue_like_illness_cum_2021,
    "Dengue virus infections, Dengue-like illness, Cum 2021†, flag" AS dengue_virus_infections_dengue_like_illness_cum_2021_flag,
    CAST("Dengue virus infections, Dengue-like illness, Cum 2020†" AS BIGINT) AS dengue_virus_infections_dengue_like_illness_cum_2020,
    "Dengue virus infections, Dengue-like illness, Cum 2020†, flag" AS dengue_virus_infections_dengue_like_illness_cum_2020_flag,
    "Dengue virus infections, Severe dengue, Current week" AS dengue_virus_infections_severe_dengue_current_week,
    "Dengue virus infections, Severe dengue, Current week, flag" AS dengue_virus_infections_severe_dengue_current_week_flag,
    CAST("Dengue virus infections, Severe dengue, Previous 52 weeks Max†" AS BIGINT) AS dengue_virus_infections_severe_dengue_previous_52_weeks_max,
    "Dengue virus infections, Severe dengue, Previous 52 weeks Max†, flag" AS dengue_virus_infections_severe_dengue_previous_52_weeks_max_flag,
    CAST("Dengue virus infections, Severe dengue,  Cum 2021†" AS BIGINT) AS dengue_virus_infections_severe_dengue_cum_2021,
    "Dengue virus infections, Severe dengue,  Cum 2021†, flag" AS dengue_virus_infections_severe_dengue_cum_2021_flag,
    CAST("Dengue virus infections, Severe dengue,  Cum 2020†" AS BIGINT) AS dengue_virus_infections_severe_dengue_cum_2020,
    "Dengue virus infections, Severe dengue, Cum 2020†, flag" AS dengue_virus_infections_severe_dengue_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-9axm-gjt8"
