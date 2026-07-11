-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "IncidentName" AS incidentname,
    "FeatureCategory" AS featurecategory,
    "Label" AS label,
    "MapMethod" AS mapmethod,
    "Comments" AS comments,
    "Angle" AS angle,
    "LatWGS84_DDM" AS latwgs84_ddm,
    "LongWGS84_DDM" AS longwgs84_ddm,
    "RepairStatus" AS repairstatus,
    "RepairComments" AS repaircomments,
    "PropertyInfo" AS propertyinfo,
    "DeleteThis" AS deletethis,
    "FeatureAccess" AS featureaccess,
    "FeatureStatus" AS featurestatus,
    "IsVisible" AS isvisible,
    "PointName" AS pointname,
    "CreateDate" AS createdate,
    "DateCurrent" AS datecurrent,
    "PointDateTime" AS pointdatetime,
    "ComplexName" AS complexname,
    "ComplexID" AS complexid,
    "GACC" AS gacc,
    "IMTName" AS imtname,
    "UnitID" AS unitid,
    "LocalIncidentID" AS localincidentid,
    "IRWINID" AS irwinid,
    "GeometryID" AS geometryid,
    "GlobalID" AS globalid,
    "GDB_ARCHIVE_OID" AS gdb_archive_oid,
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    "OBJECTID" AS objectid
FROM "nifc-2aa165c74bf040f1a44c63b505f1a940-0"
