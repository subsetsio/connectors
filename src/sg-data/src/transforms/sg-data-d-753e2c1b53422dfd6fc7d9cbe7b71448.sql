-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Below25Years_Total" AS below25years_total,
    "Below25Years_Males" AS below25years_males,
    "Below25Years_Females" AS below25years_females,
    "25_44Years_Total" AS 25_44years_total,
    "25_44Years_Males" AS 25_44years_males,
    "25_44Years_Females" AS 25_44years_females,
    "45_64Years_Total" AS 45_64years_total,
    "45_64Years_Males" AS 45_64years_males,
    "45_64Years_Females" AS 45_64years_females,
    "65YearsandOver_Total" AS 65yearsandover_total,
    "65YearsandOver_Males" AS 65yearsandover_males,
    "65YearsandOver_Females" AS 65yearsandover_females
FROM "sg-data-d-753e2c1b53422dfd6fc7d9cbe7b71448"
