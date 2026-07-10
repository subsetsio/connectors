-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Botulism, Foodborne, Current week" AS botulism_foodborne_current_week,
    "Botulism, Foodborne, Current week, flag" AS botulism_foodborne_current_week_flag,
    CAST("Botulism, Foodborne, Previous 52 weeks Max†" AS BIGINT) AS botulism_foodborne_previous_52_weeks_max,
    "Botulism, Foodborne, Previous 52 weeks Max†, flag" AS botulism_foodborne_previous_52_weeks_max_flag,
    "Botulism, Foodborne, Cum 2022†" AS botulism_foodborne_cum_2022,
    "Botulism, Foodborne, Cum 2022†, flag" AS botulism_foodborne_cum_2022_flag,
    CAST("Botulism, Foodborne, Cum 2021†" AS BIGINT) AS botulism_foodborne_cum_2021,
    "Botulism, Foodborne, Cum 2021†, flag" AS botulism_foodborne_cum_2021_flag,
    "Botulism, Infant, Current week" AS botulism_infant_current_week,
    "Botulism, Infant, Current week, flag" AS botulism_infant_current_week_flag,
    CAST("Botulism, Infant, Previous 52 weeks Max†" AS BIGINT) AS botulism_infant_previous_52_weeks_max,
    "Botulism, Infant, Previous 52 weeks Max†, flag" AS botulism_infant_previous_52_weeks_max_flag,
    CAST("Botulism, Infant, Cum 2022†" AS BIGINT) AS botulism_infant_cum_2022,
    "Botulism, Infant, Cum 2022†, flag" AS botulism_infant_cum_2022_flag,
    CAST("Botulism, Infant, Cum 2021†" AS BIGINT) AS botulism_infant_cum_2021,
    "Botulism, Infant, Cum 2021†, flag" AS botulism_infant_cum_2021_flag,
    "Botulism, Other (wound and unspecified), Current week" AS botulism_other_wound_and_unspecified_current_week,
    "Botulism, Other (wound and unspecified), Current week, flag" AS botulism_other_wound_and_unspecified_current_week_flag,
    CAST("Botulism, Other (wound and unspecified), Previous 52 weeks Max†" AS BIGINT) AS botulism_other_wound_and_unspecified_previous_52_weeks_max,
    "Botulism, Other (wound and unspecified), Previous 52 weeks Max†, flag" AS botulism_other_wound_and_unspecified_previous_52_weeks_max_flag,
    "Botulism, Other (wound and unspecified), Cum 2022†" AS botulism_other_wound_and_unspecified_cum_2022,
    "Botulism, Other (wound and unspecified), Cum 2022†, flag" AS botulism_other_wound_and_unspecified_cum_2022_flag,
    CAST("Botulism, Other (wound and unspecified), Cum 2021†" AS BIGINT) AS botulism_other_wound_and_unspecified_cum_2021,
    "Botulism, Other (wound and unspecified), Cum 2021†, flag" AS botulism_other_wound_and_unspecified_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-b6sy-qq3u"
