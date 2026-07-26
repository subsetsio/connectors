-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Salmonella Paratyphi infection§, Current week" AS salmonella_paratyphi_infection_current_week,
    "Salmonella Paratyphi infection§, Current week, flag" AS salmonella_paratyphi_infection_current_week_flag,
    CAST("Salmonella Paratyphi infection§, Previous 52 weeks Max†" AS BIGINT) AS salmonella_paratyphi_infection_previous_52_weeks_max,
    "Salmonella Paratyphi infection§, Previous 52 weeks Max†, flag" AS salmonella_paratyphi_infection_previous_52_weeks_max_flag,
    CAST("Salmonella Paratyphi infection§, Cum 2022†" AS BIGINT) AS salmonella_paratyphi_infection_cum_2022,
    "Salmonella Paratyphi infection§, Cum 2022†, flag" AS salmonella_paratyphi_infection_cum_2022_flag,
    CAST("Salmonella Paratyphi infection§, Cum 2021†" AS BIGINT) AS salmonella_paratyphi_infection_cum_2021,
    "Salmonella Paratyphi infection§, Cum 2021†, flag" AS salmonella_paratyphi_infection_cum_2021_flag,
    "Salmonella Typhi infection¶, Current week" AS salmonella_typhi_infection_current_week,
    "Salmonella Typhi infection¶, Current week, flag" AS salmonella_typhi_infection_current_week_flag,
    CAST("Salmonella Typhi infection¶, Previous 52 weeks Max†" AS BIGINT) AS salmonella_typhi_infection_previous_52_weeks_max,
    "Salmonella Typhi infection¶, Previous 52 weeks Max†, flag" AS salmonella_typhi_infection_previous_52_weeks_max_flag,
    CAST("Salmonella Typhi infection¶, Cum 2022†" AS BIGINT) AS salmonella_typhi_infection_cum_2022,
    "Salmonella Typhi infection¶, Cum 2022†, flag" AS salmonella_typhi_infection_cum_2022_flag,
    CAST("Salmonella Typhi infection¶, Cum 2021†" AS BIGINT) AS salmonella_typhi_infection_cum_2021,
    "Salmonella Typhi infection¶, Cum 2021†, flag" AS salmonella_typhi_infection_cum_2021_flag,
    CAST("Salmonellosis (excluding Salmonella Typhi infection and Salmonella Paratyphi infection)**, Current week" AS BIGINT) AS salmonella_excluding_s_typhi_inf_and_s_paratyphi_inf_curr_wk,
    "Salmonellosis (excluding Salmonella Typhi infection and Salmonella Paratyphi infection)**, Current week, flag" AS salmonella_excluding_s_typhi_inf_and_s_paratyphi_inf_cu_1fcf565d,
    CAST("Salmonellosis (excluding Salmonella Typhi infection and Salmonella Paratyphi infection)**, Previous 52 weeks Max†" AS BIGINT) AS salmonella_excluding_s_typhi_inf_and_s_paratyphi_inf_pr_00b190fc,
    "Salmonellosis (excluding Salmonella Typhi infection and Salmonella Paratyphi infection)**, Previous 52 weeks Max†, flag" AS salmonella_excluding_s_typhi_inf_and_s_paratyphi_inf_pr_b813ccdf,
    CAST("Salmonellosis (excluding Salmonella Typhi infection and Salmonella Paratyphi infection)**, Cum 2022†" AS BIGINT) AS salmonella_excluding_s_typhi_inf_and_s_paratyphi_inf_cum_2022,
    "Salmonellosis (excluding Salmonella Typhi infection and Salmonella Paratyphi infection)**, Cum 2022†, flag" AS salmonella_excluding_s_typhi_inf_and_s_paratyphi_inf_cu_66b2f1b3,
    CAST("Salmonellosis (excluding Salmonella Typhi infection and Salmonella Paratyphi infection)**, Cum 2021†" AS BIGINT) AS salmonella_excluding_s_typhi_inf_and_s_paratyphi_inf_cum_2021,
    "Salmonellosis (excluding Salmonella Typhi infection and Salmonella Paratyphi infection)**, Cum 2021†, flag" AS salmonella_excluding_s_typhi_inf_and_s_paratyphi_inf_cu_7aea9852,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-rcdh-n3ej"
