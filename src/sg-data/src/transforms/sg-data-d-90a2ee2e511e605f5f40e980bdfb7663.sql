-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Housework_Childcare_CaregivingToOthers_Total" AS housework_childcare_caregivingtoothers_total,
    "Housework_Childcare_CaregivingToOthers_Males" AS housework_childcare_caregivingtoothers_males,
    "Housework_Childcare_CaregivingToOthers_Females" AS housework_childcare_caregivingtoothers_females,
    "Retired_TooOldToWork_Total" AS retired_toooldtowork_total,
    "Retired_TooOldToWork_Males" AS retired_toooldtowork_males,
    "Retired_TooOldToWork_Females" AS retired_toooldtowork_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-90a2ee2e511e605f5f40e980bdfb7663"
