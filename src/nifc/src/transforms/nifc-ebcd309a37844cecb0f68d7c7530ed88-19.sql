-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "InteragencyName" AS interagencyname,
    "ID" AS id,
    "JoinID" AS joinid,
    "JoinFeature" AS joinfeature,
    "CreatedBy" AS createdby,
    "CreatedOnDate" AS createdondate,
    "LastModifiedBy" AS lastmodifiedby,
    "LastModifiedDate" AS lastmodifieddate,
    "GlobalID" AS globalid,
    "OBJECTID" AS objectid
FROM "nifc-ebcd309a37844cecb0f68d7c7530ed88-19"
