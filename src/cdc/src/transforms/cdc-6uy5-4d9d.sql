-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Rabies, Animal, Current week" AS BIGINT) AS rabies_animal_current_week,
    "Rabies, Animal, Current week, flag" AS rabies_animal_current_week_flag,
    CAST("Rabies, Animal, Previous 52 weeks Max†" AS BIGINT) AS rabies_animal_previous_52_weeks_max,
    "Rabies, Animal, Previous 52 weeks Max†, flag" AS rabies_animal_previous_52_weeks_max_flag,
    CAST("Rabies, Animal, Cum 2022†" AS BIGINT) AS rabies_animal_cum_2022,
    "Rabies, Animal, Cum 2022†, flag" AS rabies_animal_cum_2022_flag,
    CAST("Rabies, Animal, Cum 2021†" AS BIGINT) AS rabies_animal_cum_2021,
    "Rabies, Animal, Cum 2021†, flag" AS rabies_animal_cum_2021_flag,
    "Rabies, Human, Current week" AS rabies_human_current_week,
    "Rabies, Human, Current week, flag" AS rabies_human_current_week_flag,
    CAST("Rabies, Human, Previous 52 weeks Max†" AS BIGINT) AS rabies_human_previous_52_weeks_max,
    "Rabies, Human, Previous 52 weeks Max†, flag" AS rabies_human_previous_52_weeks_max_flag,
    "Rabies, Human, Cum 2022†" AS rabies_human_cum_2022,
    "Rabies, Human, Cum 2022†, flag" AS rabies_human_cum_2022_flag,
    "Rabies, Human, Cum 2021†" AS rabies_human_cum_2021,
    "Rabies, Human, Cum 2021†, flag" AS rabies_human_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-6uy5-4d9d"
