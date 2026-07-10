-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Viral hemorrhagic fevers§, Crimean-Congo hemorrhagic fever virus, Current week" AS viral_hemorrhagic_fevers_crimean_congo_hemorrhagic_fever_virus_current_week,
    "Viral hemorrhagic fevers§, Crimean-Congo hemorrhagic fever virus, Current week, flag" AS viral_hemorrhagic_fevers_crimean_congo_hemorrhagic_fever_virus_current_week_flag,
    CAST("Viral hemorrhagic fevers§, Crimean-Congo hemorrhagic fever virus, Previous 52 weeks Max†" AS BIGINT) AS viral_hemorrhagic_fevers_crimean_congo_hemorrhagic_fever_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Crimean-Congo hemorrhagic fever virus, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_crimean_congo_hemorrhagic_fever_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Crimean-Congo hemorrhagic fever virus, Cum 2021†" AS viral_hemorrhagic_fevers_crimean_congo_hemorrhagic_fever_virus_cum_2021,
    "Viral hemorrhagic fevers§, Crimean-Congo hemorrhagic fever virus, Cum 2021†, flag" AS viral_hemorrhagic_fevers_crimean_congo_hemorrhagic_fever_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Crimean-Congo hemorrhagic fever virus, Cum 2020†" AS viral_hemorrhagic_fevers_crimean_congo_hemorrhagic_fever_virus_cum_2020,
    "Viral hemorrhagic fevers§, Crimean-Congo hemorrhagic fever virus, Cum 2020†, flag" AS viral_hemorrhagic_fevers_crimean_congo_hemorrhagic_fever_virus_cum_2020_flag,
    "Viral hemorrhagic fevers§, Ebola virus, Current week" AS viral_hemorrhagic_fevers_ebola_virus_current_week,
    "Viral hemorrhagic fevers§, Ebola virus, Current week, flag" AS viral_hemorrhagic_fevers_ebola_virus_current_week_flag,
    CAST("Viral hemorrhagic fevers§, Ebola virus, Previous 52 weeks Max†" AS BIGINT) AS viral_hemorrhagic_fevers_ebola_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Ebola virus, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_ebola_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Ebola virus, Cum 2021†" AS viral_hemorrhagic_fevers_ebola_virus_cum_2021,
    "Viral hemorrhagic fevers§, Ebola virus, Cum 2021†, flag" AS viral_hemorrhagic_fevers_ebola_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Ebola virus, Cum 2020†" AS viral_hemorrhagic_fevers_ebola_virus_cum_2020,
    "Viral hemorrhagic fevers§, Ebola virus, Cum 2020†, flag" AS viral_hemorrhagic_fevers_ebola_virus_cum_2020_flag,
    "Viral hemorrhagic fevers§, Guanarito virus, Current week" AS viral_hemorrhagic_fevers_guanarito_virus_current_week,
    "Viral hemorrhagic fevers§, Guanarito virus, Current week, flag" AS viral_hemorrhagic_fevers_guanarito_virus_current_week_flag,
    CAST("Viral hemorrhagic fevers§, Guanarito virus, Previous 52 weeks Max†" AS BIGINT) AS viral_hemorrhagic_fevers_guanarito_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Guanarito virus, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_guanarito_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Guanarito virus, Cum 2021†" AS viral_hemorrhagic_fevers_guanarito_virus_cum_2021,
    "Viral hemorrhagic fevers§, Guanarito virus, Cum 2021†, flag" AS viral_hemorrhagic_fevers_guanarito_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Guanarito virus, Cum 2020†" AS viral_hemorrhagic_fevers_guanarito_virus_cum_2020,
    "Viral hemorrhagic fevers§, Guanarito virus, Cum 2020†, flag" AS viral_hemorrhagic_fevers_guanarito_virus_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-ppmd-3u54"
