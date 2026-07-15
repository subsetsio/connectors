-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_AgeAtFirstMarriage_Years_Below20" AS total_ageatfirstmarriage_years_below20,
    "Total_AgeAtFirstMarriage_Years_20_24" AS total_ageatfirstmarriage_years_20_24,
    "Total_AgeAtFirstMarriage_Years_25_29" AS total_ageatfirstmarriage_years_25_29,
    "Total_AgeAtFirstMarriage_Years_30_34" AS total_ageatfirstmarriage_years_30_34,
    "Total_AgeAtFirstMarriage_Years_35_39" AS total_ageatfirstmarriage_years_35_39,
    "Total_AgeAtFirstMarriage_Years_40andOver" AS total_ageatfirstmarriage_years_40andover,
    "Chinese_Total" AS chinese_total,
    "Chinese_AgeAtFirstMarriage_Years_Below20" AS chinese_ageatfirstmarriage_years_below20,
    "Chinese_AgeAtFirstMarriage_Years_20_24" AS chinese_ageatfirstmarriage_years_20_24,
    "Chinese_AgeAtFirstMarriage_Years_25_29" AS chinese_ageatfirstmarriage_years_25_29,
    "Chinese_AgeAtFirstMarriage_Years_30_34" AS chinese_ageatfirstmarriage_years_30_34,
    "Chinese_AgeAtFirstMarriage_Years_35_39" AS chinese_ageatfirstmarriage_years_35_39,
    "Chinese_AgeAtFirstMarriage_Years_40andOver" AS chinese_ageatfirstmarriage_years_40andover,
    "Malays_Total" AS malays_total,
    "Malays_AgeAtFirstMarriage_Years_Below20" AS malays_ageatfirstmarriage_years_below20,
    "Malays_AgeAtFirstMarriage_Years_20_24" AS malays_ageatfirstmarriage_years_20_24,
    "Malays_AgeAtFirstMarriage_Years_25_29" AS malays_ageatfirstmarriage_years_25_29,
    "Malays_AgeAtFirstMarriage_Years_30_34" AS malays_ageatfirstmarriage_years_30_34,
    "Malays_AgeAtFirstMarriage_Years_35_39" AS malays_ageatfirstmarriage_years_35_39,
    "Malays_AgeAtFirstMarriage_Years_40andOver" AS malays_ageatfirstmarriage_years_40andover,
    "Indians_Total" AS indians_total,
    "Indians_AgeAtFirstMarriage_Years_Below20" AS indians_ageatfirstmarriage_years_below20,
    "Indians_AgeAtFirstMarriage_Years_20_24" AS indians_ageatfirstmarriage_years_20_24,
    "Indians_AgeAtFirstMarriage_Years_25_29" AS indians_ageatfirstmarriage_years_25_29,
    "Indians_AgeAtFirstMarriage_Years_30_34" AS indians_ageatfirstmarriage_years_30_34,
    "Indians_AgeAtFirstMarriage_Years_35_39" AS indians_ageatfirstmarriage_years_35_39,
    "Indians_AgeAtFirstMarriage_Years_40andOver" AS indians_ageatfirstmarriage_years_40andover,
    "Others_Total" AS others_total,
    "Others_AgeAtFirstMarriage_Years_Below20" AS others_ageatfirstmarriage_years_below20,
    "Others_AgeAtFirstMarriage_Years_20_24" AS others_ageatfirstmarriage_years_20_24,
    "Others_AgeAtFirstMarriage_Years_25_29" AS others_ageatfirstmarriage_years_25_29,
    "Others_AgeAtFirstMarriage_Years_30_34" AS others_ageatfirstmarriage_years_30_34,
    "Others_AgeAtFirstMarriage_Years_35_39" AS others_ageatfirstmarriage_years_35_39,
    "Others_AgeAtFirstMarriage_Years_40andOver" AS others_ageatfirstmarriage_years_40andover
FROM "sg-data-d-3de421ca89ff660c9fdc00debbf9764e"
