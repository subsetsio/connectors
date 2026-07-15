-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Pre_Primary_Total" AS pre_primary_total,
    "Pre_Primary_Males" AS pre_primary_males,
    "Pre_Primary_Females" AS pre_primary_females,
    "Primary_Total" AS primary_total,
    "Primary_Males" AS primary_males,
    "Primary_Females" AS primary_females,
    "Secondary_Total" AS secondary_total,
    "Secondary_Males" AS secondary_males,
    "Secondary_Females" AS secondary_females,
    "UpperSecondary_Total" AS uppersecondary_total,
    "UpperSecondary_Males" AS uppersecondary_males,
    "UpperSecondary_Females" AS uppersecondary_females,
    "Polytechnic_Total" AS polytechnic_total,
    "Polytechnic_Males" AS polytechnic_males,
    "Polytechnic_Females" AS polytechnic_females,
    "University_Total" AS university_total,
    "University_Males" AS university_males,
    "University_Females" AS university_females
FROM "sg-data-d-0a80e1bd4cb7485d5179f23c784b14e1"
