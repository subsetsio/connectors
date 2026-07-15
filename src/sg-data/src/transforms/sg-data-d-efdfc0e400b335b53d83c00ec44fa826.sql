-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Manufacturing" AS manufacturing,
    "Construction" AS construction,
    "WholesaleandRetailTrade" AS wholesaleandretailtrade,
    "HotelsandRestaurants" AS hotelsandrestaurants,
    "TransportandStorage" AS transportandstorage,
    "InformationandCommunications" AS informationandcommunications,
    "FinancialServices" AS financialservices,
    "BusinessServices" AS businessservices,
    "Community_SocialandPersonalServices" AS community_socialandpersonalservices,
    "Others" AS others
FROM "sg-data-d-efdfc0e400b335b53d83c00ec44fa826"
