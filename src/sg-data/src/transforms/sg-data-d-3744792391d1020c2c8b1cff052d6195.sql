-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "InternetSites_OnlineAdvertisements_Total" AS internetsites_onlineadvertisements_total,
    "InternetSites_OnlineAdvertisements_Males" AS internetsites_onlineadvertisements_males,
    "InternetSites_OnlineAdvertisements_Females" AS internetsites_onlineadvertisements_females,
    "Advertisement1_WriteIn_Total" AS advertisement1_writein_total,
    "Advertisement1_WriteIn_Males" AS advertisement1_writein_males,
    "Advertisement1_WriteIn_Females" AS advertisement1_writein_females,
    "AskedFriendsorRelatives_Total" AS askedfriendsorrelatives_total,
    "AskedFriendsorRelatives_Males" AS askedfriendsorrelatives_males,
    "AskedFriendsorRelatives_Females" AS askedfriendsorrelatives_females,
    "EmploymentServices_Total" AS employmentservices_total,
    "EmploymentServices_Males" AS employmentservices_males,
    "EmploymentServices_Females" AS employmentservices_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-3744792391d1020c2c8b1cff052d6195"
