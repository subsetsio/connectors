-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Leptospirosis, Current week" AS BIGINT) AS leptospirosis_current_week,
    "Leptospirosis, Current week, flag" AS leptospirosis_current_week_flag,
    CAST("Leptospirosis, Previous 52 weeks Max†" AS BIGINT) AS leptospirosis_previous_52_weeks_max,
    "Leptospirosis, Previous 52 weeks Max†, flag" AS leptospirosis_previous_52_weeks_max_flag,
    CAST("Leptospirosis, Cum 2021†" AS BIGINT) AS leptospirosis_cum_2021,
    "Leptospirosis, Cum 2021†, flag" AS leptospirosis_cum_2021_flag,
    CAST("Leptospirosis, Cum 2020†" AS BIGINT) AS leptospirosis_cum_2020,
    "Leptospirosis, Cum 2020†, flag" AS leptospirosis_cum_2020_flag,
    CAST("Listeriosis§, Confirmed, Current week" AS BIGINT) AS listeriosis_confirmed_current_week,
    "Listeriosis§, Confirmed, Current week, flag" AS listeriosis_confirmed_current_week_flag,
    CAST("Listeriosis§, Confirmed, Previous 52 weeks Max†" AS BIGINT) AS listeriosis_confirmed_previous_52_weeks_max,
    "Listeriosis§, Confirmed, Previous 52 weeks Max†, flag" AS listeriosis_confirmed_previous_52_weeks_max_flag,
    CAST("Listeriosis§, Confirmed, Cum 2021†" AS BIGINT) AS listeriosis_confirmed_cum_2021,
    "Listeriosis§, Confirmed, Cum 2021†, flag" AS listeriosis_confirmed_cum_2021_flag,
    CAST("Listeriosis§, Confirmed, Cum 2020†" AS BIGINT) AS listeriosis_confirmed_cum_2020,
    "Listeriosis§, Confirmed, Cum 2020†, flag" AS listeriosis_confirmed_cum_2020_flag,
    CAST("Listeriosis§, Probable, Current week" AS BIGINT) AS listeriosis_probable_current_week,
    "Listeriosis§, Probable, Current week, flag" AS listeriosis_probable_current_week_flag,
    CAST("Listeriosis§, Probable, Previous 52 weeks Max†" AS BIGINT) AS listeriosis_probable_previous_52_weeks_max,
    "Listeriosis§, Probable, Previous 52 weeks Max†, flag" AS listeriosis_probable_previous_52_weeks_max_flag,
    CAST("Listeriosis§, Probable,  Cum 2021†" AS BIGINT) AS listeriosis_probable_cum_2021,
    "Listeriosis§, Probable,  Cum 2021†, flag" AS listeriosis_probable_cum_2021_flag,
    CAST("Listeriosis§, Probable,  Cum 2020†" AS BIGINT) AS listeriosis_probable_cum_2020,
    "Listeriosis§, Probable, Cum 2020†, flag" AS listeriosis_probable_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-7gnu-j6js"
