-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Manufacturing" AS manufacturing,
    "Construction" AS construction,
    "Services_Total" AS services_total,
    "Services_WholesaleandRetailTrade" AS services_wholesaleandretailtrade,
    "Services_TransportationandStorage" AS services_transportationandstorage,
    "Services_AccommodationandFoodServices" AS services_accommodationandfoodservices,
    "Services_InformationandCommunications" AS services_informationandcommunications,
    "Services_FinancialandInsuranceServices" AS services_financialandinsuranceservices,
    "Services_RealEstateServices" AS services_realestateservices,
    "Services_ProfessionalServices" AS services_professionalservices,
    "Services_AdministrativeandSupportServices" AS services_administrativeandsupportservices,
    "Services_PublicAdministrationandEducation" AS services_publicadministrationandeducation,
    "Services_HealthandSocialServices" AS services_healthandsocialservices,
    "Services_Arts_EntertainmentandRecreation" AS services_arts_entertainmentandrecreation,
    "Services_OtherCommunity_SocialandPersonalServices" AS services_othercommunity_socialandpersonalservices,
    "Others1" AS others1
FROM "sg-data-d-a9b684696b39023c4b12f13e57aa2dfd"
