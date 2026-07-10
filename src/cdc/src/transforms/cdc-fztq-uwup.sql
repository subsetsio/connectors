-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Cholera, Current week" AS cholera_current_week,
    "Cholera, Current week, flag" AS cholera_current_week_flag,
    CAST("Cholera, Previous 52 weeks Max†" AS BIGINT) AS cholera_previous_52_weeks_max,
    "Cholera, Previous 52 weeks Max†, flag" AS cholera_previous_52_weeks_max_flag,
    "Cholera, Cum 2022†" AS cholera_cum_2022,
    "Cholera, Cum 2022†, flag" AS cholera_cum_2022_flag,
    "Cholera, Cum 2021†" AS cholera_cum_2021,
    "Cholera, Cum 2021†, flag" AS cholera_cum_2021_flag,
    CAST("Coccidioidomycosis, Current week" AS BIGINT) AS coccidioidomycosis_current_week,
    "Coccidioidomycosis, Current week, flag" AS coccidioidomycosis_current_week_flag,
    CAST("Coccidioidomycosis, Previous 52 weeks Max†" AS BIGINT) AS coccidioidomycosis_previous_52_weeks_max,
    "Coccidioidomycosis, Previous 52 weeks Max†, flag" AS coccidioidomycosis_previous_52_weeks_max_flag,
    CAST("Coccidioidomycosis, Cum 2022†" AS BIGINT) AS coccidioidomycosis_cum_2022,
    "Coccidioidomycosis, Cum 2022†, flag" AS coccidioidomycosis_cum_2022_flag,
    CAST("Coccidioidomycosis, Cum 2021†" AS BIGINT) AS coccidioidomycosis_cum_2021,
    "Coccidioidomycosis, Cum 2021†, flag" AS coccidioidomycosis_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocoding"
FROM "cdc-fztq-uwup"
