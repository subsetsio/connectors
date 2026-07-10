-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("Current MMWR Year" AS BIGINT) AS current_mmwr_year,
    CAST("MMWR WEEK" AS BIGINT) AS mmwr_week,
    "Label" AS label,
    CAST("Current week" AS BIGINT) AS current_week,
    "Current week, flag" AS current_week_flag,
    CAST("Previous 52 week Max" AS BIGINT) AS previous_52_week_max,
    "Previous 52 weeks Max, flag" AS previous_52_weeks_max_flag,
    CAST("Cumulative YTD Current MMWR Year" AS BIGINT) AS cumulative_ytd_current_mmwr_year,
    "Cumulative YTD Current MMWR Year, flag" AS cumulative_ytd_current_mmwr_year_flag,
    CAST("Cumulative YTD Previous MMWR Year" AS BIGINT) AS cumulative_ytd_previous_mmwr_year,
    "Cumulative YTD Previous MMWR Year, flag" AS cumulative_ytd_previous_mmwr_year_flag,
    "LOCATION1" AS location1,
    "LOCATION2" AS location2,
    CAST("sort_order" AS BIGINT) AS sort_order,
    "geocode"
FROM "cdc-x9gk-5huc"
