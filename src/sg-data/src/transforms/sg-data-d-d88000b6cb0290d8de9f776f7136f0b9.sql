-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "15_19Years_Total" AS 15_19years_total,
    "15_19Years_Males" AS 15_19years_males,
    "15_19Years_Females" AS 15_19years_females,
    "20_24Years_Total" AS 20_24years_total,
    "20_24Years_Males" AS 20_24years_males,
    "20_24Years_Females" AS 20_24years_females,
    "25_29Years_Total" AS 25_29years_total,
    "25_29Years_Males" AS 25_29years_males,
    "25_29Years_Females" AS 25_29years_females,
    "30_34Years_Total" AS 30_34years_total,
    "30_34Years_Males" AS 30_34years_males,
    "30_34Years_Females" AS 30_34years_females,
    "35_39Years_Total" AS 35_39years_total,
    "35_39Years_Males" AS 35_39years_males,
    "35_39Years_Females" AS 35_39years_females,
    "40_44Years_Total" AS 40_44years_total,
    "40_44Years_Males" AS 40_44years_males,
    "40_44Years_Females" AS 40_44years_females,
    "45_49Years_Total" AS 45_49years_total,
    "45_49Years_Males" AS 45_49years_males,
    "45_49Years_Females" AS 45_49years_females,
    "50_54Years_Total" AS 50_54years_total,
    "50_54Years_Males" AS 50_54years_males,
    "50_54Years_Females" AS 50_54years_females,
    "55_59Years_Total" AS 55_59years_total,
    "55_59Years_Males" AS 55_59years_males,
    "55_59Years_Females" AS 55_59years_females,
    "60_64Years_Total" AS 60_64years_total,
    "60_64Years_Males" AS 60_64years_males,
    "60_64Years_Females" AS 60_64years_females,
    "65YearsandOver_Total" AS 65yearsandover_total,
    "65YearsandOver_Males" AS 65yearsandover_males,
    "65YearsandOver_Females" AS 65yearsandover_females
FROM "sg-data-d-d88000b6cb0290d8de9f776f7136f0b9"
