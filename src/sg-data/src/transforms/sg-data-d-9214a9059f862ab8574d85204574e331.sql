-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Tamil_Total" AS tamil_total,
    "Tamil_Males" AS tamil_males,
    "Tamil_Females" AS tamil_females,
    "Malayalee_Total" AS malayalee_total,
    "Malayalee_Males" AS malayalee_males,
    "Malayalee_Females" AS malayalee_females,
    "Hindi_Total" AS hindi_total,
    "Hindi_Males" AS hindi_males,
    "Hindi_Females" AS hindi_females,
    "Sikh_Total" AS sikh_total,
    "Sikh_Males" AS sikh_males,
    "Sikh_Females" AS sikh_females,
    "Punjabi_Total" AS punjabi_total,
    "Punjabi_Males" AS punjabi_males,
    "Punjabi_Females" AS punjabi_females,
    "Urdu_Total" AS urdu_total,
    "Urdu_Males" AS urdu_males,
    "Urdu_Females" AS urdu_females,
    "Hindustani_Total" AS hindustani_total,
    "Hindustani_Males" AS hindustani_males,
    "Hindustani_Females" AS hindustani_females,
    "Gujarati_Total" AS gujarati_total,
    "Gujarati_Males" AS gujarati_males,
    "Gujarati_Females" AS gujarati_females,
    "Sindhi_Total" AS sindhi_total,
    "Sindhi_Males" AS sindhi_males,
    "Sindhi_Females" AS sindhi_females,
    "Sinhalese_Total" AS sinhalese_total,
    "Sinhalese_Males" AS sinhalese_males,
    "Sinhalese_Females" AS sinhalese_females,
    "OtherIndians_Total" AS otherindians_total,
    "OtherIndians_Males" AS otherindians_males,
    "OtherIndians_Females" AS otherindians_females
FROM "sg-data-d-9214a9059f862ab8574d85204574e331"
