-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Hansen's Disease, Current week" AS BIGINT) AS hansen_s_disease_current_week,
    "Hansen's Disease, Current week, flag" AS hansen_s_disease_current_week_flag,
    CAST("Hansen's Disease, Previous 52 weeks Max†" AS BIGINT) AS hansen_s_disease_previous_52_weeks_max,
    "Hansen's Disease, Previous 52 weeks Max†, flag" AS hansen_s_disease_previous_52_weeks_max_flag,
    CAST("Hansen's Disease, Cum 2021†" AS BIGINT) AS hansen_s_disease_cum_2021,
    "Hansen's Disease, Cum 2021†, flag" AS hansen_s_disease_cum_2021_flag,
    CAST("Hansen's Disease, Cum 2020†" AS BIGINT) AS hansen_s_disease_cum_2020,
    "Hansen's Disease, Cum 2020†, flag" AS hansen_s_disease_cum_2020_flag,
    "Hantavirus infection, non-hantavirus pulmonary syndrome§, Current week" AS hantavirus_infection_non_hantavirus_pulmonary_syndrome_current_week,
    "Hantavirus infection, non-hantavirus pulmonary syndrome§, Current week, flag" AS hantavirus_infection_non_hantavirus_pulmonary_syndrome_current_week_flag,
    CAST("Hantavirus infection, non-hantavirus pulmonary syndrome§, Previous 52 weeks Max†" AS BIGINT) AS hantavirus_infection_non_hantavirus_pulmonary_syndrome_previous_52_weeks_max,
    "Hantavirus infection, non-hantavirus pulmonary syndrome§, Previous 52 weeks Max†, flag" AS hantavirus_infection_non_hantavirus_pulmonary_syndrome_previous_52_weeks_max_flag,
    CAST("Hantavirus infection, non-hantavirus pulmonary syndrome§, Cum 2021†" AS BIGINT) AS hantavirus_infection_non_hantavirus_pulmonary_syndrome_cum_2021,
    "Hantavirus infection, non-hantavirus pulmonary syndrome§, Cum 2021†, flag" AS hantavirus_infection_non_hantavirus_pulmonary_syndrome_cum_2021_flag,
    CAST("Hantavirus infection, non-hantavirus pulmonary syndrome§, Cum 2020†" AS BIGINT) AS hantavirus_infection_non_hantavirus_pulmonary_syndrome_cum_2020,
    "Hantavirus infection, non-hantavirus pulmonary syndrome§, Cum 2020†, flag" AS hantavirus_infection_non_hantavirus_pulmonary_syndrome_cum_2020_flag,
    "Hantavirus pulmonary syndrome¶, Current week" AS hantavirus_pulmonary_syndrome_current_week,
    "Hantavirus pulmonary syndrome¶, Current week, flag" AS hantavirus_pulmonary_syndrome_current_week_flag,
    CAST("Hantavirus pulmonary syndrome¶, Previous 52 weeks Max†" AS BIGINT) AS hantavirus_pulmonary_syndrome_previous_52_weeks_max,
    "Hantavirus pulmonary syndrome¶, Previous 52 weeks Max†, flag" AS hantavirus_pulmonary_syndrome_previous_52_weeks_max_flag,
    CAST("Hantavirus pulmonary syndrome¶, Cum 2021†" AS BIGINT) AS hantavirus_pulmonary_syndrome_cum_2021,
    "Hantavirus pulmonary syndrome¶, Cum 2021†, flag" AS hantavirus_pulmonary_syndrome_cum_2021_flag,
    CAST("Hantavirus pulmonary syndrome¶, Cum 2020†" AS BIGINT) AS hantavirus_pulmonary_syndrome_cum_2020,
    "Hantavirus pulmonary syndrome¶, Cum 2020†, flag" AS hantavirus_pulmonary_syndrome_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-chmz-4uae"
