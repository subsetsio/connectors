-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Manufacturing" AS total_manufacturing,
    "Total_Construction" AS total_construction,
    "Total_WholesaleandRetailTrade" AS total_wholesaleandretailtrade,
    "Total_HotelsandRestaurants" AS total_hotelsandrestaurants,
    "Total_TransportandStorage" AS total_transportandstorage,
    "Total_InformationandCommunications" AS total_informationandcommunications,
    "Total_FinancialServices" AS total_financialservices,
    "Total_BusinessServices" AS total_businessservices,
    "Total_Community_SocialandPersonalServices" AS total_community_socialandpersonalservices,
    "Total_Others" AS total_others,
    "Males_Total" AS males_total,
    "Males_Manufacturing" AS males_manufacturing,
    "Males_Construction" AS males_construction,
    "Males_WholesaleandRetailTrade" AS males_wholesaleandretailtrade,
    "Males_HotelsandRestaurants" AS males_hotelsandrestaurants,
    "Males_TransportandStorage" AS males_transportandstorage,
    "Males_InformationandCommunications" AS males_informationandcommunications,
    "Males_FinancialServices" AS males_financialservices,
    "Males_BusinessServices" AS males_businessservices,
    "Males_Community_SocialandPersonalServices" AS males_community_socialandpersonalservices,
    "Males_Others" AS males_others,
    "Females_Total" AS females_total,
    "Females_Manufacturing" AS females_manufacturing,
    "Females_Construction" AS females_construction,
    "Females_WholesaleandRetailTrade" AS females_wholesaleandretailtrade,
    "Females_HotelsandRestaurants" AS females_hotelsandrestaurants,
    "Females_TransportandStorage" AS females_transportandstorage,
    "Females_InformationandCommunications" AS females_informationandcommunications,
    "Females_FinancialServices" AS females_financialservices,
    "Females_BusinessServices" AS females_businessservices,
    "Females_Community_SocialandPersonalServices" AS females_community_socialandpersonalservices,
    "Females_Others" AS females_others
FROM "sg-data-d-d1d60da4ee50d0a9b6cb92cbd4cd8578"
