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
    "EconomicallyActive_Total" AS economicallyactive_total,
    "EconomicallyActive_AgeAtFirstMarriage_Years_Below20" AS economicallyactive_ageatfirstmarriage_years_below20,
    "EconomicallyActive_AgeAtFirstMarriage_Years_20_24" AS economicallyactive_ageatfirstmarriage_years_20_24,
    "EconomicallyActive_AgeAtFirstMarriage_Years_25_29" AS economicallyactive_ageatfirstmarriage_years_25_29,
    "EconomicallyActive_AgeAtFirstMarriage_Years_30_34" AS economicallyactive_ageatfirstmarriage_years_30_34,
    "EconomicallyActive_AgeAtFirstMarriage_Years_35_39" AS economicallyactive_ageatfirstmarriage_years_35_39,
    "EconomicallyActive_AgeAtFirstMarriage_Years_40andOver" AS economicallyactive_ageatfirstmarriage_years_40andover,
    "EconomicallyInactive_Total" AS economicallyinactive_total,
    "EconomicallyInactive_AgeAtFirstMarriage_Years_Below20" AS economicallyinactive_ageatfirstmarriage_years_below20,
    "EconomicallyInactive_AgeAtFirstMarriage_Years_20_24" AS economicallyinactive_ageatfirstmarriage_years_20_24,
    "EconomicallyInactive_AgeAtFirstMarriage_Years_25_29" AS economicallyinactive_ageatfirstmarriage_years_25_29,
    "EconomicallyInactive_AgeAtFirstMarriage_Years_30_34" AS economicallyinactive_ageatfirstmarriage_years_30_34,
    "EconomicallyInactive_AgeAtFirstMarriage_Years_35_39" AS economicallyinactive_ageatfirstmarriage_years_35_39,
    "EconomicallyInactive_AgeAtFirstMarriage_Years_40andOver" AS economicallyinactive_ageatfirstmarriage_years_40andover
FROM "sg-data-d-35c918481922f672c8dfefacfe690541"
