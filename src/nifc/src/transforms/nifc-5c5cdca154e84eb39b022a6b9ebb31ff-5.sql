-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SourceGlobalID" AS sourceglobalid,
    "SourceOID" AS sourceoid,
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    "OBJECTID" AS objectid,
    "IncidentName" AS incidentname,
    "FeatureCategory" AS featurecategory,
    "MapMethod" AS mapmethod,
    "Comments" AS comments,
    "Label" AS label,
    "RepairStatus" AS repairstatus,
    "RepairsNeeded" AS repairsneeded,
    "RepairComments" AS repaircomments,
    "RepairPriority" AS repairpriority,
    "ArchClearance" AS archclearance,
    "DeleteThis" AS deletethis,
    "FeatureAccess" AS featureaccess,
    "FeatureStatus" AS featurestatus,
    "IsVisible" AS isvisible,
    "LineDateTime" AS linedatetime,
    "CreateDate" AS createdate,
    "DateCurrent" AS datecurrent,
    "LengthFeet" AS lengthfeet,
    "LineWidthFeet" AS linewidthfeet,
    "IRWINID" AS irwinid,
    "GISS_Misc" AS giss_misc,
    "GISS_Misc2" AS giss_misc2,
    "Shape__Length" AS shape_length
FROM "nifc-5c5cdca154e84eb39b022a6b9ebb31ff-5"
