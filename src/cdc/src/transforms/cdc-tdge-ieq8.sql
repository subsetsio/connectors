-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Q fever, Total, Current week" AS BIGINT) AS q_fever_total_current_week,
    "Q fever, Total, Current week, flag" AS q_fever_total_current_week_flag,
    CAST("Q fever, Total, Previous 52 weeks Max†" AS BIGINT) AS q_fever_total_previous_52_weeks_max,
    "Q fever, Total, Previous 52 weeks Max†, flag" AS q_fever_total_previous_52_weeks_max_flag,
    CAST("Q fever, Total, Cum 2021†" AS BIGINT) AS q_fever_total_cum_2021,
    "Q fever, Total, Cum 2021†, flag" AS q_fever_total_cum_2021_flag,
    CAST("Q fever, Total, Cum 2020†" AS BIGINT) AS q_fever_total_cum_2020,
    "Q fever, Total, Cum 2020†, flag" AS q_fever_total_cum_2020_flag,
    CAST("Q fever, Acute, Current week" AS BIGINT) AS q_fever_acute_current_week,
    "Q fever, Acute, Current week, flag" AS q_fever_acute_current_week_flag,
    CAST("Q fever, Acute, Previous 52 weeks Max†" AS BIGINT) AS q_fever_acute_previous_52_weeks_max,
    "Q fever, Acute, Previous 52 weeks Max†, flag" AS q_fever_acute_previous_52_weeks_max_flag,
    CAST("Q fever, Acute, Cum 2021†" AS BIGINT) AS q_fever_acute_cum_2021,
    "Q fever, Acute, Cum 2021†, flag" AS q_fever_acute_cum_2021_flag,
    CAST("Q fever, Acute, Cum 2020†" AS BIGINT) AS q_fever_acute_cum_2020,
    "Q fever, Acute, Cum 2020†, flag" AS q_fever_acute_cum_2020_flag,
    CAST("Q fever, Chronic, Current week" AS BIGINT) AS q_fever_chronic_current_week,
    "Q fever, Chronic, Current week, flag" AS q_fever_chronic_current_week_flag,
    CAST("Q fever, Chronic, Previous 52 weeks Max†" AS BIGINT) AS q_fever_chronic_previous_52_weeks_max,
    "Q fever, Chronic, Previous 52 weeks Max†, flag" AS q_fever_chronic_previous_52_weeks_max_flag,
    CAST("Q fever, Chronic, Cum 2021†" AS BIGINT) AS q_fever_chronic_cum_2021,
    "Q fever, Chronic, Cum 2021†, flag" AS q_fever_chronic_cum_2021_flag,
    CAST("Q fever, Chronic, Cum 2020†" AS BIGINT) AS q_fever_chronic_cum_2020,
    "Q fever, Chronic, Cum 2020†, flag" AS q_fever_chronic_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-tdge-ieq8"
