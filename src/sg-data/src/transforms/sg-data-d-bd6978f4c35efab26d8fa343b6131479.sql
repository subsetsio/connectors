-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "EmploymentService_Total" AS employmentservice_total,
    "EmploymentService_Males" AS employmentservice_males,
    "EmploymentService_Females" AS employmentservice_females,
    "Advertisement_WriteIn_Total" AS advertisement_writein_total,
    "Advertisement_WriteIn_Males" AS advertisement_writein_males,
    "Advertisement_WriteIn_Females" AS advertisement_writein_females,
    "AskedFriendsOrRelatives_Total" AS askedfriendsorrelatives_total,
    "AskedFriendsOrRelatives_Males" AS askedfriendsorrelatives_males,
    "AskedFriendsOrRelatives_Females" AS askedfriendsorrelatives_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-bd6978f4c35efab26d8fa343b6131479"
