-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "EntityType" AS entitytype,
    CAST("EntityID" AS BIGINT) AS entityid,
    "Reason" AS reason,
    "CurrentFiscalYear" AS currentfiscalyear,
    "TargetFiscalYear" AS targetfiscalyear,
    "ModifiedDate" AS modifieddate,
    "CreatedOnDate" AS createdondate,
    "IsArchived" AS isarchived,
    "GeometryType" AS geometrytype,
    "Notes" AS notes,
    "GlobalID" AS globalid,
    "ID" AS id,
    "JoinID" AS joinid,
    "JoinFeature" AS joinfeature
FROM "nifc-ebcd309a37844cecb0f68d7c7530ed88-13"
