-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SourceGlobalID" AS sourceglobalid,
    "GDB_FROM_DATE" AS gdb_from_date,
    "GDB_TO_DATE" AS gdb_to_date,
    "SourceOID" AS sourceoid,
    "OBJECTID" AS objectid,
    "IncidentName" AS incidentname,
    "FeatureCategory" AS featurecategory,
    "Comments" AS comments,
    "FeatureAccess" AS featureaccess,
    "FeatureStatus" AS featurestatus,
    "IsVisible" AS isvisible,
    "Label" AS label,
    "ContainmentStrategy" AS containmentstrategy,
    "CreateDate" AS createdate,
    "DateCurrent" AS datecurrent,
    "LengthFeet" AS lengthfeet,
    "IRWINID" AS irwinid,
    "GISS_Misc" AS giss_misc,
    "GlobalID" AS globalid,
    "Shape__Length" AS shape_length
FROM "nifc-696c45c4ecd34948b1ae87d2f567e347-6"
