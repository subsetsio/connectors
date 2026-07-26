-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Current week" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_471cda94,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Current week, flag" AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_365df414,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Previous 52 weeks Max†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_cf1d7330,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Previous 52 weeks Max†, flag" AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_8e9cfa28,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Cum 2021†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_8963ff12,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Cum 2021†, flag" AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_4e9a4b7f,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Cum 2020†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_59ee0830,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Confirmed, Cum 2020†, flag" AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_e7b04a84,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Current week" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_e88ab2d9,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Current week, flag" AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_019f4f5f,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Previous 52 weeks Max†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_324c8445,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Previous 52 weeks Max†, flag" AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_af2f7b90,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Cum 2021†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_e4f9b159,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Cum 2021†, flag" AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_7fa2bb6c,
    CAST("Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Cum 2020†" AS BIGINT) AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_eb31a346,
    "Vibriosis (any species of the family Vibrionaceae, other than toxigenic Vibrio cholerae O1 or O139), Probable, Cum 2020†, flag" AS vibriosis_any_species_of_the_family_vibrio_not_tox_vibr_06771632,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-vq7a-fvin"
