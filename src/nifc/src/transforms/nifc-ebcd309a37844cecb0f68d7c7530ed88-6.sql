-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GlobalID_STR" AS globalid_str,
    "TreatmentActivityGroupName" AS treatmentactivitygroupname,
    "IsArchived" AS isarchived,
    "CreatedDate" AS createddate,
    "GlobalID" AS globalid,
    "ID" AS id
FROM "nifc-ebcd309a37844cecb0f68d7c7530ed88-6"
