-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The actor catalog can contain repeated or partially blank actor-name rows for one actor identifier; treat it as a source roster rather than a unique actor dimension.
SELECT
    "ActorId" AS actorid,
    "NameData" AS namedata,
    "NameOrig" AS nameorig,
    "NameOrigFull" AS nameorigfull,
    "NameOrigFullEng" AS nameorigfulleng,
    "NameChange" AS namechange,
    "NewName" AS newname,
    "NewNameFullMotherTongue" AS newnamefullmothertongue,
    "NewNameFullEng" AS newnamefulleng,
    "Org" AS org,
    "ConflictId" AS conflictid,
    "DyadId" AS dyadid,
    "PrimaryParty" AS primaryparty,
    "OSID" AS osid,
    "OSCoalition" AS oscoalition,
    "OSCoalitionID" AS oscoalitionid,
    "NSID" AS nsid,
    "NSCoalition" AS nscoalition,
    "NSCoalitionID" AS nscoalitionid,
    "Splinter" AS splinter,
    "NamePrev" AS nameprev,
    "ActorIdPrev" AS actoridprev,
    "SplitTemp" AS splittemp,
    "NameSplitTemp" AS namesplittemp,
    "ActorIdSplitTemp" AS actoridsplittemp,
    "Alliance" AS alliance,
    "NameAlliance" AS namealliance,
    "ActorIdAlliance" AS actoridalliance,
    "JoinGroup" AS joingroup,
    "GroupName" AS groupname,
    "ActorIdGroup" AS actoridgroup,
    "Location" AS location,
    "GWNOLoc" AS gwnoloc,
    "Region" AS region,
    "Version" AS version
FROM "ucdp-actor"
