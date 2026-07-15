-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "AnsweredAdvertisements_Total" AS answeredadvertisements_total,
    "AnsweredAdvertisements_Males" AS answeredadvertisements_males,
    "AnsweredAdvertisements_Females" AS answeredadvertisements_females,
    "AskedFriends_Relatives_Total" AS askedfriends_relatives_total,
    "AskedFriends_Relatives_Males" AS askedfriends_relatives_males,
    "AskedFriends_Relatives_Females" AS askedfriends_relatives_females,
    "RegisteredWithEmploymentAgencies_Total" AS registeredwithemploymentagencies_total,
    "RegisteredWithEmploymentAgencies_Males" AS registeredwithemploymentagencies_males,
    "RegisteredWithEmploymentAgencies_Females" AS registeredwithemploymentagencies_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-d377d7485a4dc842798cb69eae6bb9db"
