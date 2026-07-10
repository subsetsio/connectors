-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "subapplicationIdentifier" AS subapplicationidentifier,
    "communityName" AS communityname,
    "county",
    "stateAbbreviation" AS stateabbreviation,
    "communityNumber" AS communitynumber,
    "countyCode" AS countycode,
    "stateNumberCode" AS statenumbercode,
    "isCrsCommunity" AS iscrscommunity,
    "crsRating" AS crsrating,
    "congressionalDistrict" AS congressionaldistrict,
    "id"
FROM "fema-hmasubapplicationsbynfipcrscommunities"
