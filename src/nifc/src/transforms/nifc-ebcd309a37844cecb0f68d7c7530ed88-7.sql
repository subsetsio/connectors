-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TreatmentActivityGroupItemsID" AS treatmentactivitygroupitemsid,
    "TreatmentActivityGroupID" AS treatmentactivitygroupid,
    "TreatmentID" AS treatmentid,
    "ActivityID" AS activityid,
    "SequenceNumber" AS sequencenumber,
    "IsArchived" AS isarchived,
    "EntityType" AS entitytype,
    "EntityID" AS entityid,
    "GeometryType" AS geometrytype,
    "CreatedDate" AS createddate,
    "GlobalID" AS globalid,
    "ID" AS id,
    "JoinID" AS joinid,
    "JoinFeature" AS joinfeature,
    "TreatmentActivityGroupJoinID" AS treatmentactivitygroupjoinid,
    "OBJECTID" AS objectid
FROM "nifc-ebcd309a37844cecb0f68d7c7530ed88-7"
