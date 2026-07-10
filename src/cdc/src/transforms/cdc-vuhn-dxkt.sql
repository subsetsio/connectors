-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Poliovirus infection, nonparalytic, Current week" AS poliovirus_infection_nonparalytic_current_week,
    "Poliovirus infection, nonparalytic, Current week, flag" AS poliovirus_infection_nonparalytic_current_week_flag,
    CAST("Poliovirus infection, nonparalytic, Previous 52 weeks Max†" AS BIGINT) AS poliovirus_infection_nonparalytic_previous_52_weeks_max,
    "Poliovirus infection, nonparalytic, Previous 52 weeks Max†, flag" AS poliovirus_infection_nonparalytic_previous_52_weeks_max_flag,
    "Poliovirus infection, nonparalytic, Cum 2022†" AS poliovirus_infection_nonparalytic_cum_2022,
    "Poliovirus infection, nonparalytic, Cum 2022†, flag" AS poliovirus_infection_nonparalytic_cum_2022_flag,
    "Poliovirus infection, nonparalytic, Cum 2021†" AS poliovirus_infection_nonparalytic_cum_2021,
    "Poliovirus infection, nonparalytic, Cum 2021†, flag" AS poliovirus_infection_nonparalytic_cum_2021_flag,
    "Psittacosis, Current week" AS psittacosis_current_week,
    "Psittacosis, Current week, flag" AS psittacosis_current_week_flag,
    CAST("Psittacosis, Previous 52 weeks Max†" AS BIGINT) AS psittacosis_previous_52_weeks_max,
    "Psittacosis, Previous 52 weeks Max†, flag" AS psittacosis_previous_52_weeks_max_flag,
    "Psittacosis, Cum 2022†" AS psittacosis_cum_2022,
    "Psittacosis, Cum 2022†, flag" AS psittacosis_cum_2022_flag,
    CAST("Psittacosis, Cum 2021†" AS BIGINT) AS psittacosis_cum_2021,
    "Psittacosis, Cum 2021†, flag" AS psittacosis_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-vuhn-dxkt"
