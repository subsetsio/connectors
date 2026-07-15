-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "65_69Years_Total" AS 65_69years_total,
    "65_69Years_Males" AS 65_69years_males,
    "65_69Years_Females" AS 65_69years_females,
    "70_74Years_Total" AS 70_74years_total,
    "70_74Years_Males" AS 70_74years_males,
    "70_74Years_Females" AS 70_74years_females,
    "75_79Years_Total" AS 75_79years_total,
    "75_79Years_Males" AS 75_79years_males,
    "75_79Years_Females" AS 75_79years_females,
    "80YearsAndOver_Total" AS 80yearsandover_total,
    "80YearsAndOver_Males" AS 80yearsandover_males,
    "80YearsAndOver_Females" AS 80yearsandover_females
FROM "sg-data-d-7fb6d91e0212e155c0d5f31843f54cf3"
