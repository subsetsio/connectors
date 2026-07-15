-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Working_Total" AS working_total,
    "Working_Males" AS working_males,
    "Working_Females" AS working_females,
    "Unemployed_Total" AS unemployed_total,
    "Unemployed_Males" AS unemployed_males,
    "Unemployed_Females" AS unemployed_females
FROM "sg-data-d-1cf02cbafc6a4099b5943d0c552ad761"
