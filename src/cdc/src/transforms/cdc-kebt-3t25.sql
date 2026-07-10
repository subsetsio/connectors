-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Pertussis, Current week" AS BIGINT) AS pertussis_current_week,
    "Pertussis, Current week, flag" AS pertussis_current_week_flag,
    CAST("Pertussis, Previous 52 weeks Max†" AS BIGINT) AS pertussis_previous_52_weeks_max,
    "Pertussis, Previous 52 weeks Max†, flag" AS pertussis_previous_52_weeks_max_flag,
    CAST("Pertussis, Cum 2021†" AS BIGINT) AS pertussis_cum_2021,
    "Pertussis, Cum 2021†, flag" AS pertussis_cum_2021_flag,
    CAST("Pertussis, Cum 2020†" AS BIGINT) AS pertussis_cum_2020,
    "Pertussis, Cum 2020†, flag" AS pertussis_cum_2020_flag,
    "Plague, Current week" AS plague_current_week,
    "Plague, Current week, flag" AS plague_current_week_flag,
    CAST("Plague, Previous 52 weeks Max†" AS BIGINT) AS plague_previous_52_weeks_max,
    "Plague, Previous 52 weeks Max†, flag" AS plague_previous_52_weeks_max_flag,
    CAST("Plague, Cum 2021†" AS BIGINT) AS plague_cum_2021,
    "Plague, Cum 2021†, flag" AS plague_cum_2021_flag,
    CAST("Plague, Cum 2020†" AS BIGINT) AS plague_cum_2020,
    "Plague, Cum 2020†, flag" AS plague_cum_2020_flag,
    "Poliomyelitis, paralytic, Current week" AS poliomyelitis_paralytic_current_week,
    "Poliomyelitis, paralytic, Current week, flag" AS poliomyelitis_paralytic_current_week_flag,
    CAST("Poliomyelitis, paralytic, Previous 52 weeks Max†" AS BIGINT) AS poliomyelitis_paralytic_previous_52_weeks_max,
    "Poliomyelitis, paralytic, Previous 52 weeks Max†, flag" AS poliomyelitis_paralytic_previous_52_weeks_max_flag,
    "Poliomyelitis, paralytic, Cum 2021†" AS poliomyelitis_paralytic_cum_2021,
    "Poliomyelitis, paralytic, Cum 2021†, flag" AS poliomyelitis_paralytic_cum_2021_flag,
    "Poliomyelitis, paralytic, Cum 2020†" AS poliomyelitis_paralytic_cum_2020,
    "Poliomyelitis, paralytic, Cum 2020†, flag" AS poliomyelitis_paralytic_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-kebt-3t25"
