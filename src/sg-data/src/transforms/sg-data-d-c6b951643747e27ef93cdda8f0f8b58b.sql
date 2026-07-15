-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Single_Total" AS single_total,
    "Single_Males" AS single_males,
    "Single_Females" AS single_females,
    "Married_Total" AS married_total,
    "Married_Males" AS married_males,
    "Married_Females" AS married_females,
    "Widowed_Total" AS widowed_total,
    "Widowed_Males" AS widowed_males,
    "Widowed_Females" AS widowed_females,
    "Divorced_Separated_Total" AS divorced_separated_total,
    "Divorced_Separated_Males" AS divorced_separated_males,
    "Divorced_Separated_Females" AS divorced_separated_females
FROM "sg-data-d-c6b951643747e27ef93cdda8f0f8b58b"
