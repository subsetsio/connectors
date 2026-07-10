-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "communityIdNumber" AS communityidnumber,
    "communityName" AS communityname,
    "county",
    "state",
    "initialFloodHazardBoundaryMap" AS initialfloodhazardboundarymap,
    "initialFloodInsuranceRateMap" AS initialfloodinsuranceratemap,
    "currentlyEffectiveMapDate" AS currentlyeffectivemapdate,
    "regularEmergencyProgramDate" AS regularemergencyprogramdate,
    "tribal",
    "participatingInNFIP" AS participatinginnfip,
    "originalEntryDate" AS originalentrydate,
    "classRatingEffectiveDate" AS classratingeffectivedate,
    "classRating" AS classrating,
    "sfhaDiscount" AS sfhadiscount,
    "nonSfhaDiscount" AS nonsfhadiscount,
    "lastRefresh" AS lastrefresh
FROM "fema-nfipcommunitystatusbook"
