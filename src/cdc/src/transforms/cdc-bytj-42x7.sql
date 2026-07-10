-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Viral hemorrhagic fevers§, Guanarito virus¶, Current week" AS viral_hemorrhagic_fevers_guanarito_virus_current_week,
    "Viral hemorrhagic fevers§, Guanarito virus¶, Current week, flag" AS viral_hemorrhagic_fevers_guanarito_virus_current_week_flag,
    "Viral hemorrhagic fevers§, Guanarito virus¶, Previous 52 weeks Max†" AS viral_hemorrhagic_fevers_guanarito_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Guanarito virus¶, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_guanarito_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Guanarito virus¶, Cum 2022†" AS viral_hemorrhagic_fevers_guanarito_virus_cum_2022,
    "Viral hemorrhagic fevers§, Guanarito virus¶, Cum 2022†, flag" AS viral_hemorrhagic_fevers_guanarito_virus_cum_2022_flag,
    "Viral hemorrhagic fevers§, Guanarito virus¶, Cum 2021†" AS viral_hemorrhagic_fevers_guanarito_virus_cum_2021,
    "Viral hemorrhagic fevers§, Guanarito virus¶, Cum 2021†, flag" AS viral_hemorrhagic_fevers_guanarito_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Junin virus **, Current week" AS viral_hemorrhagic_fevers_junin_virus_current_week,
    "Viral hemorrhagic fevers§, Junin virus **, Current week, flag" AS viral_hemorrhagic_fevers_junin_virus_current_week_flag,
    "Viral hemorrhagic fevers§, Junin virus **, Previous 52 weeks Max†" AS viral_hemorrhagic_fevers_junin_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Junin virus **, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_junin_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Junin virus **, Cum 2022†" AS viral_hemorrhagic_fevers_junin_virus_cum_2022,
    "Viral hemorrhagic fevers§, Junin virus **, Cum 2022†, flag" AS viral_hemorrhagic_fevers_junin_virus_cum_2022_flag,
    "Viral hemorrhagic fevers§, Junin virus **, Cum 2021†" AS viral_hemorrhagic_fevers_junin_virus_cum_2021,
    "Viral hemorrhagic fevers§, Junin virus **, Cum 2021†, flag" AS viral_hemorrhagic_fevers_junin_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Lassa virus††, Current week" AS viral_hemorrhagic_fevers_lassa_virus_current_week,
    "Viral hemorrhagic fevers§, Lassa virus††, Current week, flag" AS viral_hemorrhagic_fevers_lassa_virus_current_week_flag,
    "Viral hemorrhagic fevers§, Lassa virus††, Previous 52 weeks Max†" AS viral_hemorrhagic_fevers_lassa_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Lassa virus††, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_lassa_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Lassa virus††, Cum 2022†" AS viral_hemorrhagic_fevers_lassa_virus_cum_2022,
    "Viral hemorrhagic fevers§, Lassa virus††, Cum 2022†, flag" AS viral_hemorrhagic_fevers_lassa_virus_cum_2022_flag,
    "Viral hemorrhagic fevers§, Lassa virus††, Cum 2021†" AS viral_hemorrhagic_fevers_lassa_virus_cum_2021,
    "Viral hemorrhagic fevers§, Lassa virus††, Cum 2021†, flag" AS viral_hemorrhagic_fevers_lassa_virus_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-bytj-42x7"
