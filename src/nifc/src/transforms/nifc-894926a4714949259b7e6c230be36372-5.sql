-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    "SourceOID" AS sourceoid,
    "SourceGlobalID" AS sourceglobalid,
    "OBJECTID" AS objectid,
    "IncidentName" AS incidentname,
    "FeatureCategory" AS featurecategory,
    "Comments" AS comments,
    "Label" AS label,
    "FeatureAccess" AS featureaccess,
    "FeatureStatus" AS featurestatus,
    "IsVisible" AS isvisible,
    "ManagementStrategy" AS managementstrategy,
    "LineDateTime" AS linedatetime,
    "CreateDate" AS createdate,
    "DateCurrent" AS datecurrent,
    "LengthFeet" AS lengthfeet,
    "IRWINID" AS irwinid,
    "CpxName" AS cpxname,
    "GISS_Misc" AS giss_misc,
    "GlobalID" AS globalid,
    "Shape__Length" AS shape_length
FROM "nifc-894926a4714949259b7e6c230be36372-5"
