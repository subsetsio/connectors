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
    "80_84Years_Total" AS 80_84years_total,
    "80_84Years_Males" AS 80_84years_males,
    "80_84Years_Females" AS 80_84years_females,
    "85YearsandOver_Total" AS 85yearsandover_total,
    "85YearsandOver_Males" AS 85yearsandover_males,
    "85YearsandOver_Females" AS 85yearsandover_females
FROM "sg-data-d-1c920964239f97903b8ad15bdb793e59"
