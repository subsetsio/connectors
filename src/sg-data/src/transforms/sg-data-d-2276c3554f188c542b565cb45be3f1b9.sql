-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
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
    "OtherIndians_Total" AS otherindians_total,
    "OtherIndians_Males" AS otherindians_males,
    "OtherIndians_Females" AS otherindians_females
FROM "sg-data-d-2276c3554f188c542b565cb45be3f1b9"
