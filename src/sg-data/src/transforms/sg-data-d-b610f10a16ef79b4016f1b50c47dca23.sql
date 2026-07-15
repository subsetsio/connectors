-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Housework_Childcare_CaregivingtoOthers_Total" AS housework_childcare_caregivingtoothers_total,
    "Housework_Childcare_CaregivingtoOthers_Males" AS housework_childcare_caregivingtoothers_males,
    "Housework_Childcare_CaregivingtoOthers_Females" AS housework_childcare_caregivingtoothers_females,
    "Retired_TooOldtoWork_Total" AS retired_toooldtowork_total,
    "Retired_TooOldtoWork_Males" AS retired_toooldtowork_males,
    "Retired_TooOldtoWork_Females" AS retired_toooldtowork_females,
    "PoorHealth_Disabled_Total" AS poorhealth_disabled_total,
    "PoorHealth_Disabled_Males" AS poorhealth_disabled_males,
    "PoorHealth_Disabled_Females" AS poorhealth_disabled_females,
    "Education_TrainingRelated1_Total" AS education_trainingrelated1_total,
    "Education_TrainingRelated1_Males" AS education_trainingrelated1_males,
    "Education_TrainingRelated1_Females" AS education_trainingrelated1_females,
    "TakingaBreak_Total" AS takingabreak_total,
    "TakingaBreak_Males" AS takingabreak_males,
    "TakingaBreak_Females" AS takingabreak_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-b610f10a16ef79b4016f1b50c47dca23"
