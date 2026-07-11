-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "EntityType" AS entitytype,
    "EntityID" AS entityid,
    "CancelReason" AS cancelreason,
    "CancelSubReason" AS cancelsubreason,
    "HasSubstitute" AS hassubstitute,
    "SubstituteEntityType" AS substituteentitytype,
    "SubstituteEntityID" AS substituteentityid,
    "ModifiedDate" AS modifieddate,
    "CreatedOnDate" AS createdondate,
    "IsArchived" AS isarchived,
    "GeometryType" AS geometrytype,
    "GlobalID" AS globalid,
    "ID" AS id,
    "JoinID" AS joinid,
    "JoinFeature" AS joinfeature,
    "JoinIDS" AS joinids,
    "JoinFeatureS" AS joinfeatures
FROM "nifc-ebcd309a37844cecb0f68d7c7530ed88-16"
