-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "IncidentName" AS incidentname,
    "FeatureCategory" AS featurecategory,
    "MapMethod" AS mapmethod,
    "Comments" AS comments,
    "RepairStatus" AS repairstatus,
    "RepairComments" AS repaircomments,
    "DeleteThis" AS deletethis,
    "FeatureAccess" AS featureaccess,
    "FeatureStatus" AS featurestatus,
    "IsVisible" AS isvisible,
    "Label" AS label,
    "LineDateTime" AS linedatetime,
    "CreateDate" AS createdate,
    "DateCurrent" AS datecurrent,
    "ComplexName" AS complexname,
    "ComplexID" AS complexid,
    "GACC" AS gacc,
    "IMTName" AS imtname,
    "LengthFeet" AS lengthfeet,
    "UnitID" AS unitid,
    "LocalIncidentID" AS localincidentid,
    "IRWINID" AS irwinid,
    "GeometryID" AS geometryid,
    "GlobalID" AS globalid,
    "LineWidthFeet" AS linewidthfeet,
    "ArchClearance" AS archclearance,
    "OBJECTID" AS objectid,
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    CAST("ORIGINAL_OBJECTID" AS BIGINT) AS original_objectid,
    "SHAPE__Length" AS shape_length
FROM "nifc-2827d083ddc14464a8eab3181e8bf13e-0"
