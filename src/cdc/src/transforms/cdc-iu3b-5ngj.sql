-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Rubella, Current week" AS BIGINT) AS rubella_current_week,
    "Rubella, Current week, flag" AS rubella_current_week_flag,
    CAST("Rubella, Previous 52 weeks Max†" AS BIGINT) AS rubella_previous_52_weeks_max,
    "Rubella, Previous 52 weeks Max†, flag" AS rubella_previous_52_weeks_max_flag,
    CAST("Rubella, Cum 2021†" AS BIGINT) AS rubella_cum_2021,
    "Rubella, Cum 2021†, flag" AS rubella_cum_2021_flag,
    CAST("Rubella, Cum 2020†" AS BIGINT) AS rubella_cum_2020,
    "Rubella, Cum 2020†, flag" AS rubella_cum_2020_flag,
    "Rubella, congenital syndrome, Current week" AS rubella_congenital_syndrome_current_week,
    "Rubella, congenital syndrome, Current week, flag" AS rubella_congenital_syndrome_current_week_flag,
    CAST("Rubella, congenital syndrome, Previous 52 weeks Max†" AS BIGINT) AS rubella_congenital_syndrome_previous_52_weeks_max,
    "Rubella, congenital syndrome, Previous 52 weeks Max†, flag" AS rubella_congenital_syndrome_previous_52_weeks_max_flag,
    "Rubella, congenital syndrome, Cum 2021†" AS rubella_congenital_syndrome_cum_2021,
    "Rubella, congenital syndrome, Cum 2021†, flag" AS rubella_congenital_syndrome_cum_2021_flag,
    "Rubella, congenital syndrome, Cum 2020†" AS rubella_congenital_syndrome_cum_2020,
    "Rubella, congenital syndrome, Cum 2020†, flag" AS rubella_congenital_syndrome_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-iu3b-5ngj"
