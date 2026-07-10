-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Current week" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_confirmed_current_week,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Current week, flag" AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_confirmed_current_week_flag,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Previous 52 weeks Max†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_confirmed_previous_52_weeks_max,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Previous 52 weeks Max†, flag" AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_confirmed_previous_52_weeks_max_flag,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Cum 2021†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_confirmed_cum_2021,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Cum 2021†, flag" AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_confirmed_cum_2021_flag,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Cum 2020†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_confirmed_cum_2020,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Cum 2020†, flag" AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_confirmed_cum_2020_flag,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Current week" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_probable_current_week,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Current week, flag" AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_probable_current_week_flag,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Previous 52 weeks Max†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_probable_previous_52_weeks_max,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Previous 52 weeks Max†, flag" AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_probable_previous_52_weeks_max_flag,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Cum 2021†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_probable_cum_2021,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Cum 2021†, flag" AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_probable_cum_2021_flag,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Cum 2020†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_probable_cum_2020,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Cum 2020†, flag" AS vibriosis_any_species_of_the_family_vibrionaceae_other_than_toxigenic_vibrio_cholerae_o1_or_o139_probable_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-vq7a-fvin"
