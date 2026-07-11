-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Date" AS date,
    "HB" AS hb,
    CAST("HealthcareCdiffInfection" AS BIGINT) AS healthcarecdiffinfection,
    "HealthcareCdiffInfectionQF" AS healthcarecdiffinfectionqf,
    CAST("HealthcareEcoliBacteraemia" AS BIGINT) AS healthcareecolibacteraemia,
    "HealthcareEcoliBacteraemiaQF" AS healthcareecolibacteraemiaqf,
    CAST("HealthcareSaureusBacteraemia" AS BIGINT) AS healthcaresaureusbacteraemia,
    "HealthcareSaureusBacteraemiaQF" AS healthcaresaureusbacteraemiaqf,
    CAST("HealthcareTotalOccupiedBedDays" AS BIGINT) AS healthcaretotaloccupiedbeddays,
    "HealthcareTotalOccupiedBedDaysQF" AS healthcaretotaloccupiedbeddaysqf,
    CAST("CommunityCdiffInfection" AS BIGINT) AS communitycdiffinfection,
    "CommunityCdiffInfectionQF" AS communitycdiffinfectionqf,
    CAST("CommunityEcoliBacteraemia" AS BIGINT) AS communityecolibacteraemia,
    "CommunityEcoliBacteraemiaQF" AS communityecolibacteraemiaqf,
    CAST("CommunitySaureusBacteraemia" AS BIGINT) AS communitysaureusbacteraemia,
    "CommunitySaureusBacteraemiaQF" AS communitysaureusbacteraemiaqf,
    CAST("CommunityAnnualisedPopulation" AS DOUBLE) AS communityannualisedpopulation,
    "CommunityAnnualisedPopulationQF" AS communityannualisedpopulationqf,
    CAST("HipArthroplastySSI" AS BIGINT) AS hiparthroplastyssi,
    "HipArthroplastySSIQF" AS hiparthroplastyssiqf,
    CAST("HipArthroplastyProcedures" AS BIGINT) AS hiparthroplastyprocedures,
    "HipArthroplastyProceduresQF" AS hiparthroplastyproceduresqf,
    CAST("CsectionSSI" AS BIGINT) AS csectionssi,
    "CsectionSSIQF" AS csectionssiqf,
    CAST("CsectionProcedures" AS BIGINT) AS csectionprocedures,
    "CsectionProceduresQF" AS csectionproceduresqf
FROM "public-health-scotland-quarterly-epidemiological-data-on-healthcare-associated-infections"
