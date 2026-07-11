-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PlannedTreatmentObjectID" AS plannedtreatmentobjectid,
    "ActualTreatmentObjectID" AS actualtreatmentobjectid,
    "IsArchived" AS isarchived,
    "PlannedGeometryType" AS plannedgeometrytype,
    "ActualGeometryType" AS actualgeometrytype,
    "CreatedDate" AS createddate,
    "ID" AS id,
    "JoinIDE" AS joinide,
    "JoinIDA" AS joinida,
    "JoinFeatureE" AS joinfeaturee,
    "JoinFeatureA" AS joinfeaturea,
    "PlannedActivityObjectID" AS plannedactivityobjectid,
    "ActualActivityObjectID" AS actualactivityobjectid,
    "GlobalID" AS globalid,
    "OBJECTID" AS objectid
FROM "nifc-ebcd309a37844cecb0f68d7c7530ed88-5"
