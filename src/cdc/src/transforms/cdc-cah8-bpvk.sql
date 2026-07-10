-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Viral hemorrhagic fevers§, Lujo virus¶, Current week" AS viral_hemorrhagic_fevers_lujo_virus_current_week,
    "Viral hemorrhagic fevers§, Lujo virus¶, Current week, flag" AS viral_hemorrhagic_fevers_lujo_virus_current_week_flag,
    "Viral hemorrhagic fevers§, Lujo virus¶, Previous 52 weeks Max†" AS viral_hemorrhagic_fevers_lujo_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Lujo virus¶, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_lujo_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Lujo virus¶, Cum 2022†" AS viral_hemorrhagic_fevers_lujo_virus_cum_2022,
    "Viral hemorrhagic fevers§, Lujo virus¶, Cum 2022†, flag" AS viral_hemorrhagic_fevers_lujo_virus_cum_2022_flag,
    "Viral hemorrhagic fevers§, Lujo virus¶, Cum 2021†" AS viral_hemorrhagic_fevers_lujo_virus_cum_2021,
    "Viral hemorrhagic fevers§, Lujo virus¶, Cum 2021†, flag" AS viral_hemorrhagic_fevers_lujo_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Machupo virus**, Current week" AS viral_hemorrhagic_fevers_machupo_virus_current_week,
    "Viral hemorrhagic fevers§, Machupo virus**, Current week, flag" AS viral_hemorrhagic_fevers_machupo_virus_current_week_flag,
    "Viral hemorrhagic fevers§, Machupo virus**, Previous 52 weeks Max†" AS viral_hemorrhagic_fevers_machupo_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Machupo virus**, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_machupo_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Machupo virus**, Cum 2022†" AS viral_hemorrhagic_fevers_machupo_virus_cum_2022,
    "Viral hemorrhagic fevers§, Machupo virus**, Cum 2022†, flag" AS viral_hemorrhagic_fevers_machupo_virus_cum_2022_flag,
    "Viral hemorrhagic fevers§, Machupo virus**, Cum 2021†" AS viral_hemorrhagic_fevers_machupo_virus_cum_2021,
    "Viral hemorrhagic fevers§, Machupo virus**, Cum 2021†, flag" AS viral_hemorrhagic_fevers_machupo_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Marburg virus††, Current week" AS viral_hemorrhagic_fevers_marburg_virus_current_week,
    "Viral hemorrhagic fevers§, Marburg virus††, Current week, flag" AS viral_hemorrhagic_fevers_marburg_virus_current_week_flag,
    "Viral hemorrhagic fevers§, Marburg virus††, Previous 52 weeks Max†" AS viral_hemorrhagic_fevers_marburg_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Marburg virus††, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_marburg_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Marburg virus††, Cum 2022†" AS viral_hemorrhagic_fevers_marburg_virus_cum_2022,
    "Viral hemorrhagic fevers§, Marburg virus††, Cum 2022†, flag" AS viral_hemorrhagic_fevers_marburg_virus_cum_2022_flag,
    "Viral hemorrhagic fevers§, Marburg virus††, Cum 2021†" AS viral_hemorrhagic_fevers_marburg_virus_cum_2021,
    "Viral hemorrhagic fevers§, Marburg virus††, Cum 2021†, flag" AS viral_hemorrhagic_fevers_marburg_virus_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-cah8-bpvk"
