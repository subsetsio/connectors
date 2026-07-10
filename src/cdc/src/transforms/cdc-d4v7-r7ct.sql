-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Cryptosporidiosis, Current week" AS BIGINT) AS cryptosporidiosis_current_week,
    "Cryptosporidiosis, Current week, flag" AS cryptosporidiosis_current_week_flag,
    CAST("Cryptosporidiosis, Previous 52 weeks Max†" AS BIGINT) AS cryptosporidiosis_previous_52_weeks_max,
    "Cryptosporidiosis, Previous 52 weeks Max†, flag" AS cryptosporidiosis_previous_52_weeks_max_flag,
    CAST("Cryptosporidiosis, Cum 2022†" AS BIGINT) AS cryptosporidiosis_cum_2022,
    "Cryptosporidiosis, Cum 2022†, flag" AS cryptosporidiosis_cum_2022_flag,
    CAST("Cryptosporidiosis, Cum 2021†" AS BIGINT) AS cryptosporidiosis_cum_2021,
    "Cryptosporidiosis, Cum 2021†, flag" AS cryptosporidiosis_cum_2021_flag,
    CAST("Cyclosporiasis, Current week" AS BIGINT) AS cyclosporiasis_current_week,
    "Cyclosporiasis, Current week, flag" AS cyclosporiasis_current_week_flag,
    CAST("Cyclosporiasis, Previous 52 weeks Max†" AS BIGINT) AS cyclosporiasis_previous_52_weeks_max,
    "Cyclosporiasis, Previous 52 weeks Max†, flag" AS cyclosporiasis_previous_52_weeks_max_flag,
    CAST("Cyclosporiasis, Cum 2022†" AS BIGINT) AS cyclosporiasis_cum_2022,
    "Cyclosporiasis, Cum 2022†, flag" AS cyclosporiasis_cum_2022_flag,
    CAST("Cyclosporiasis, Cum 2021†" AS BIGINT) AS cyclosporiasis_cum_2021,
    "Cyclosporiasis, Cum 2021†, flag" AS cyclosporiasis_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocoding"
FROM "cdc-d4v7-r7ct"
