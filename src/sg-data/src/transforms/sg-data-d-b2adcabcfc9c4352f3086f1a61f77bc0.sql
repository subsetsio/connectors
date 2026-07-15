-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Below30Years_Total" AS below30years_total,
    "Below30Years_Males" AS below30years_males,
    "Below30Years_Females" AS below30years_females,
    "30_39Years_Total" AS 30_39years_total,
    "30_39Years_Males" AS 30_39years_males,
    "30_39Years_Females" AS 30_39years_females,
    "40_49Years_Total" AS 40_49years_total,
    "40_49Years_Males" AS 40_49years_males,
    "40_49Years_Females" AS 40_49years_females,
    "50YearsandOver_Total" AS 50yearsandover_total,
    "50YearsandOver_Males" AS 50yearsandover_males,
    "50YearsandOver_Females" AS 50yearsandover_females
FROM "sg-data-d-b2adcabcfc9c4352f3086f1a61f77bc0"
