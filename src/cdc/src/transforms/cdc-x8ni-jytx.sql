-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Viral hemorrhagic fevers§, Junin virus, Current week" AS viral_hemorrhagic_fevers_junin_virus_current_week,
    "Viral hemorrhagic fevers§, Junin virus, Current week, flag" AS viral_hemorrhagic_fevers_junin_virus_current_week_flag,
    CAST("Viral hemorrhagic fevers§, Junin virus, Previous 52 weeks Max†" AS BIGINT) AS viral_hemorrhagic_fevers_junin_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Junin virus, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_junin_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Junin virus, Cum 2021†" AS viral_hemorrhagic_fevers_junin_virus_cum_2021,
    "Viral hemorrhagic fevers§, Junin virus, Cum 2021†, flag" AS viral_hemorrhagic_fevers_junin_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Junin virus, Cum 2020†" AS viral_hemorrhagic_fevers_junin_virus_cum_2020,
    "Viral hemorrhagic fevers§, Junin virus, Cum 2020†, flag" AS viral_hemorrhagic_fevers_junin_virus_cum_2020_flag,
    "Viral hemorrhagic fevers§, Lassa virus, Current week" AS viral_hemorrhagic_fevers_lassa_virus_current_week,
    "Viral hemorrhagic fevers§, Lassa virus, Current week, flag" AS viral_hemorrhagic_fevers_lassa_virus_current_week_flag,
    CAST("Viral hemorrhagic fevers§, Lassa virus, Previous 52 weeks Max†" AS BIGINT) AS viral_hemorrhagic_fevers_lassa_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Lassa virus, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_lassa_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Lassa virus, Cum 2021†" AS viral_hemorrhagic_fevers_lassa_virus_cum_2021,
    "Viral hemorrhagic fevers§, Lassa virus, Cum 2021†, flag" AS viral_hemorrhagic_fevers_lassa_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Lassa virus, Cum 2020†" AS viral_hemorrhagic_fevers_lassa_virus_cum_2020,
    "Viral hemorrhagic fevers§, Lassa virus, Cum 2020†, flag" AS viral_hemorrhagic_fevers_lassa_virus_cum_2020_flag,
    "Viral hemorrhagic fevers§, Lujo virus, Current week" AS viral_hemorrhagic_fevers_lujo_virus_current_week,
    "Viral hemorrhagic fevers§, Lujo virus, Current week, flag" AS viral_hemorrhagic_fevers_lujo_virus_current_week_flag,
    CAST("Viral hemorrhagic fevers§, Lujo virus, Previous 52 weeks Max†" AS BIGINT) AS viral_hemorrhagic_fevers_lujo_virus_previous_52_weeks_max,
    "Viral hemorrhagic fevers§, Lujo virus, Previous 52 weeks Max†, flag" AS viral_hemorrhagic_fevers_lujo_virus_previous_52_weeks_max_flag,
    "Viral hemorrhagic fevers§, Lujo virus, Cum 2021†" AS viral_hemorrhagic_fevers_lujo_virus_cum_2021,
    "Viral hemorrhagic fevers§, Lujo virus, Cum 2021†, flag" AS viral_hemorrhagic_fevers_lujo_virus_cum_2021_flag,
    "Viral hemorrhagic fevers§, Lujo virus, Cum 2020†" AS viral_hemorrhagic_fevers_lujo_virus_cum_2020,
    "Viral hemorrhagic fevers§, Lujo virus, Cum 2020†, flag" AS viral_hemorrhagic_fevers_lujo_virus_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-x8ni-jytx"
