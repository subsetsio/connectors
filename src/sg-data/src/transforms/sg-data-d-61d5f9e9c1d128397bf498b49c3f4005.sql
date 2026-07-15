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
    "Advertisements_WroteIn_Total" AS advertisements_wrotein_total,
    "Advertisements_WroteIn_Males" AS advertisements_wrotein_males,
    "Advertisements_WroteIn_Females" AS advertisements_wrotein_females,
    "AskedFriendsOrRelatives_Total" AS askedfriendsorrelatives_total,
    "AskedFriendsOrRelatives_Males" AS askedfriendsorrelatives_males,
    "AskedFriendsOrRelatives_Females" AS askedfriendsorrelatives_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-61d5f9e9c1d128397bf498b49c3f4005"
