-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Mumps, Current week" AS BIGINT) AS mumps_current_week,
    "Mumps, Current week, flag" AS mumps_current_week_flag,
    CAST("Mumps, Previous 52 weeks Max†" AS BIGINT) AS mumps_previous_52_weeks_max,
    "Mumps, Previous 52 weeks Max†, flag" AS mumps_previous_52_weeks_max_flag,
    CAST("Mumps, Cum 2022†" AS BIGINT) AS mumps_cum_2022,
    "Mumps, Cum 2022†, flag" AS mumps_cum_2022_flag,
    CAST("Mumps, Cum 2021†" AS BIGINT) AS mumps_cum_2021,
    "Mumps, Cum 2021†, flag" AS mumps_cum_2021_flag,
    "Novel influenza A virus infections§, Current week" AS novel_influenza_a_virus_infections_current_week,
    "Novel influenza A virus infections§, Current week, flag" AS novel_influenza_a_virus_infections_current_week_flag,
    CAST("Novel influenza A virus infections§, Previous 52 weeks Max†" AS BIGINT) AS novel_influenza_a_virus_infections_previous_52_weeks_max,
    "Novel influenza A virus infections§, Previous 52 weeks Max†, flag" AS novel_influenza_a_virus_infections_previous_52_weeks_max_flag,
    "Novel influenza A virus infections§, Cum 2022†" AS novel_influenza_a_virus_infections_cum_2022,
    "Novel influenza A virus infections§, Cum 2022†, flag" AS novel_influenza_a_virus_infections_cum_2022_flag,
    "Novel influenza A virus infections§, Cum 2021†" AS novel_influenza_a_virus_infections_cum_2021,
    "Novel influenza A virus infections§, Cum 2021†, flag" AS novel_influenza_a_virus_infections_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-kxvg-q6s7"
