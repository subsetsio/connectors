-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "IncidentName" AS incidentname,
    "FeatureCategory" AS featurecategory,
    "Label" AS label,
    "MapMethod" AS mapmethod,
    "Comments" AS comments,
    "Angle" AS angle,
    "ElevationFeet" AS elevationfeet,
    "LatWGS84_DDM" AS latwgs84_ddm,
    "LongWGS84_DDM" AS longwgs84_ddm,
    "RepairStatus" AS repairstatus,
    "RepairsNeeded" AS repairsneeded,
    "RepairComments" AS repaircomments,
    "RepairPriority" AS repairpriority,
    "ArchClearance" AS archclearance,
    "DeleteThis" AS deletethis,
    "FeatureAccess" AS featureaccess,
    "FeatureStatus" AS featurestatus,
    "IsVisible" AS isvisible,
    "PointName" AS pointname,
    "PointDateTime" AS pointdatetime,
    "CreateDate" AS createdate,
    "DateCurrent" AS datecurrent,
    "IRWINID" AS irwinid,
    "GISS_Misc" AS giss_misc,
    "GISS_Misc2" AS giss_misc2,
    "GlobalID" AS globalid,
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    "SourceGlobalID" AS sourceglobalid,
    "SourceOID" AS sourceoid
FROM "nifc-705b14551df6417aaea99dd7a651d9ff-2"
