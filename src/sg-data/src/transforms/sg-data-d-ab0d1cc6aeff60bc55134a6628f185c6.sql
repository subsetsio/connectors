-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_AgeAtFirstMarriage_Years_Below20" AS total_ageatfirstmarriage_years_below20,
    "Total_AgeAtFirstMarriage_Years_20_24" AS total_ageatfirstmarriage_years_20_24,
    "Total_AgeAtFirstMarriage_Years_25_29" AS total_ageatfirstmarriage_years_25_29,
    "Total_AgeAtFirstMarriage_Years_30_34" AS total_ageatfirstmarriage_years_30_34,
    "Total_AgeAtFirstMarriage_Years_35_39" AS total_ageatfirstmarriage_years_35_39,
    "Total_AgeAtFirstMarriage_Years_40andOver" AS total_ageatfirstmarriage_years_40andover,
    "SingaporeCitizens_Total" AS singaporecitizens_total,
    "SingaporeCitizens_AgeAtFirstMarriage_Years_Below20" AS singaporecitizens_ageatfirstmarriage_years_below20,
    "SingaporeCitizens_AgeAtFirstMarriage_Years_20_24" AS singaporecitizens_ageatfirstmarriage_years_20_24,
    "SingaporeCitizens_AgeAtFirstMarriage_Years_25_29" AS singaporecitizens_ageatfirstmarriage_years_25_29,
    "SingaporeCitizens_AgeAtFirstMarriage_Years_30_34" AS singaporecitizens_ageatfirstmarriage_years_30_34,
    "SingaporeCitizens_AgeAtFirstMarriage_Years_35_39" AS singaporecitizens_ageatfirstmarriage_years_35_39,
    "SingaporeCitizens_AgeAtFirstMarriage_Years_40andOver" AS singaporecitizens_ageatfirstmarriage_years_40andover,
    "PermanentResidents_Total" AS permanentresidents_total,
    "PermanentResidents_AgeAtFirstMarriage_Years_Below20" AS permanentresidents_ageatfirstmarriage_years_below20,
    "PermanentResidents_AgeAtFirstMarriage_Years_20_24" AS permanentresidents_ageatfirstmarriage_years_20_24,
    "PermanentResidents_AgeAtFirstMarriage_Years_25_29" AS permanentresidents_ageatfirstmarriage_years_25_29,
    "PermanentResidents_AgeAtFirstMarriage_Years_30_34" AS permanentresidents_ageatfirstmarriage_years_30_34,
    "PermanentResidents_AgeAtFirstMarriage_Years_35_39" AS permanentresidents_ageatfirstmarriage_years_35_39,
    "PermanentResidents_AgeAtFirstMarriage_Years_40andOver" AS permanentresidents_ageatfirstmarriage_years_40andover
FROM "sg-data-d-ab0d1cc6aeff60bc55134a6628f185c6"
