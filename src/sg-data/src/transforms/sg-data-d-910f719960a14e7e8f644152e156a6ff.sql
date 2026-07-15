-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "5_9Years_Total" AS 5_9years_total,
    "5_9Years_Males" AS 5_9years_males,
    "5_9Years_Females" AS 5_9years_females,
    "10_14Years_Total" AS 10_14years_total,
    "10_14Years_Males" AS 10_14years_males,
    "10_14Years_Females" AS 10_14years_females,
    "15_19Years_Total" AS 15_19years_total,
    "15_19Years_Males" AS 15_19years_males,
    "15_19Years_Females" AS 15_19years_females,
    "20YearsandOver_Total" AS 20yearsandover_total,
    "20YearsandOver_Males" AS 20yearsandover_males,
    "20YearsandOver_Females" AS 20yearsandover_females
FROM "sg-data-d-910f719960a14e7e8f644152e156a6ff"
